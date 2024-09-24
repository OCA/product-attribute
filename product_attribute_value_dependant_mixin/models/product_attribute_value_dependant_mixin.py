# Copyright 2023 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import itertools
import json

from odoo import api, fields, models


class AttributeValueDependantMixin(models.AbstractModel):
    _name = "attribute.value.dependant.mixin"
    _description = "Attribute Value Dependant Mixin"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        domain="[('id', 'in', available_product_ids)]",
    )
    available_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Available Products",
        compute="_compute_available_product_ids",
    )

    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Attribute Values",
    )

    available_attribute_value_domain = fields.Char(
        compute="_compute_available_attribute_value_domain",
    )

    @api.depends("product_tmpl_id")
    def _compute_available_product_ids(self):
        for rec in self:
            rec.available_product_ids = self.env["product.product"].search(
                [("product_tmpl_id", "=", self.product_tmpl_id._origin.id)]
            )

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.attribute_line_ids.value_ids",
        "available_attribute_value_domain",
    )
    def _compute_available_attribute_value_ids(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.available_attribute_value_ids = rec.product_tmpl_id.mapped(
                    "attribute_line_ids.value_ids"
                ).filtered_domain(json.loads(rec.available_attribute_value_domain))
            else:
                rec.available_attribute_value_ids = None

    @api.depends("product_tmpl_id", "product_tmpl_id.attribute_line_ids.value_ids")
    def _compute_available_attribute_value_domain(self):
        for rec in self:
            domain = []
            if rec.product_tmpl_id:
                domain = [
                    ("id", "in", rec.product_tmpl_id.attribute_line_ids.value_ids.ids)
                ]
            rec.available_attribute_value_domain = json.dumps(domain)

    def is_matching_product(self, product):
        self.ensure_one()
        if self.product_tmpl_id != product.product_tmpl_id:
            return False
        elif self.product_id:
            if self.product_id == product:
                return True
            else:
                return False
        elif self.attribute_value_ids:
            ptav = product.product_template_attribute_value_ids
            attr2vals = {
                attribute: set(values)
                for attribute, values in itertools.groupby(
                    self.attribute_value_ids, lambda pav: pav.attribute_id
                )
            }
            for attribute in attr2vals:
                if attribute not in ptav.attribute_id:
                    return False
                elif not attr2vals[attribute] & set(ptav.product_attribute_value_id):
                    return False
        return True
