# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductWeightUpdate(models.TransientModel):
    _name = "product.weight.update"
    _description = "Update Product Weight"

    product_tmpl_id = fields.Many2one("product.template", "Template")
    product_id = fields.Many2one("product.product", "Product")
    bom_id = fields.Many2one(
        "mrp.bom", "BoM", domain="[('product_tmpl_id', '=', product_tmpl_id)]"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if not fields:
            return res
        context = self.env.context
        if context.get("active_model") == "product.template":
            product_tmpl_id = context.get("active_id", False)
            product_id = False
            domain_template = [("product_tmpl_id", "=", product_tmpl_id)]
            domain_product = []
        else:
            product_id = context.get("active_id", False)
            product = self.env["product.product"].browse(product_id)
            product_tmpl_id = product.product_tmpl_id.id
            domain_template = [("product_tmpl_id", "=", product_tmpl_id)]
            domain_product = [("product_id", "=", product_id)]
        bom = False
        if domain_product:
            bom = self.env["mrp.bom"].search(domain_product, limit=1)
        if not domain_product or not bom:
            bom = self.env["mrp.bom"].search(domain_template, limit=1)
        if bom:
            res.update({"bom_id": bom.id})

        if "product_tmpl_id" in fields:
            res.update({"product_tmpl_id": product_tmpl_id})
        if "product_id" in fields and product_id:
            res.update({"product_id": product_id})
        return res

    def calculate_product_bom_weight(self, bom, product=False):
        product_tmpl = bom.product_tmpl_id
        if not product:
            product = product_tmpl.product_variant_ids[:1]
            if not product:
                raise UserError(
                    _(
                        "Missing active variant for product %s"
                        % (product_tmpl.display_name)
                    )
                )
        factor = product_tmpl.uom_id._compute_quantity(
            1, bom.product_uom_id, round=False
        )

        factor = 1.0 / bom.product_uom_id._compute_quantity(
            bom.product_qty, product_tmpl.uom_id, round=False
        )

        dummy, lines_info = bom.explode(product, factor)
        weight = 0.0
        for bom_line, info in lines_info:
            component = bom_line.product_id
            component_qty = bom_line.product_uom_id._compute_quantity(
                info.get("qty"), component.uom_id
            )
            weight += (
                self._get_component_weight(component, product_tmpl) * component_qty
            )
        if product:
            _logger.info("%s : %0.2f", product.name, weight)
            product.write({"weight": weight})
        else:
            _logger.info("%s : %0.2f", product_tmpl.name, weight)
            product_tmpl.write({"weight": weight})

    def update_single_weight(self):
        self.ensure_one()
        product = self.product_id or self.bom_id.product_id
        self.calculate_product_bom_weight(self.bom_id, product=product)
        return {}

    def update_multi_product_weight(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        context = self.env.context
        if context.get("active_model") == "product.template":
            template_ids = context.get("active_ids", [])
            product_ids = []
            template_obj = self.env["product.template"]
        else:
            product_ids = context.get("active_ids", [])
            template_ids = []
            product_obj = self.env["product.product"]

        # Case wizard is called from product.product tree view
        for product_id in product_ids:
            product = product_obj.browse(product_id)
            bom = self.env["mrp.bom"].search([("product_id", "=", product_id)], limit=1)
            if not bom:
                bom = self.env["mrp.bom"].search(
                    [
                        ("product_tmpl_id", "=", product.product_tmpl_id.id),
                        ("product_id", "=", False),
                    ],
                    limit=1,
                )
            if bom:
                self.calculate_product_bom_weight(bom, product=product)

        # Case wizard is called from product.template tree view
        for template_id in template_ids:
            template = template_obj.browse(template_id)
            if len(template.product_variant_ids) > 1:
                continue
            bom = self.env["mrp.bom"].search(
                [("product_tmpl_id", "=", template_id)], limit=1
            )
            if bom:
                self.calculate_product_bom_weight(bom, bom.product_id)

    def _get_component_weight(self, component, product_tmpl_id):
        """Weight according to product_tmpl_id's weight uom"""
        return component.weight
