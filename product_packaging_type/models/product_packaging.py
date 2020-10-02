# -*- coding: utf-8 -*-
# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from collections import OrderedDict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackaging(models.Model):
    _inherit = "product.packaging"
    _order = "product_tmpl_id, type_sequence"

    def default_packaging_type_id(self):
        return self.env["product.packaging.type"].search(
            [("is_default", "=", True)], limit=1
        )

    packaging_type_id = fields.Many2one(
        "product.packaging.type",
        required=True,
        ondelete="restrict",
        default=lambda p: p.default_packaging_type_id(),
    )
    barcode_required_for_gtin = fields.Boolean(
        readonly=True, compute="_compute_barcode_required_for_gtin"
    )
    type_sequence = fields.Integer(
        string="Type sequence",
        related="packaging_type_id.sequence",
        readonly=True,
        store=True,
    )
    qty_per_type = fields.Html(
        compute="_compute_qty_per_type", string="Qty per package type"
    )
    product_uom_id = fields.Many2one(
        "product.uom", related="product_tmpl_id.uom_id", readonly=True
    )

    @api.constrains("packaging_type_id", "product_tmpl_id")
    def _check_one_packaging_type_per_product(self):
        for packaging in self:
            product = packaging.product_tmpl_id
            # do not use a mapped/filtered because it would union the duplicates
            packaging_type_ids = [
                packaging.packaging_type_id.id
                for packaging in product.packaging_ids
                # We have to allow several packaging using the default type,
                # because when we install the module on an existing database,
                # the default value will be set to default and we'll have
                # duplicates. Anyway "default" is not meant to be used as a
                # real type.
                if not packaging.packaging_type_id.is_default
            ]
            if len(set(packaging_type_ids)) != len(packaging_type_ids):
                raise ValidationError(
                    _(
                        "It is forbidden to have different packagings "
                        "with the same type for a given product ({})."
                    ).format(product.display_name)
                )

    @api.depends("packaging_type_id", "packaging_type_id.has_gtin", "qty")
    def _compute_barcode_required_for_gtin(self):
        for packaging in self:
            packaging.barcode_required_for_gtin = (
                packaging.packaging_type_id.has_gtin
            )
            if not packaging.qty:
                packaging.barcode_required_for_gtin = False

    @api.depends(
        "qty",
        "product_tmpl_id",
        "product_tmpl_id.packaging_ids",
        "packaging_type_id",
        "packaging_type_id.code",
    )
    def _compute_qty_per_type(self):
        for packaging in self:
            product = packaging.product_tmpl_id
            if not product:
                packaging.qty_per_type = ""
                continue

            smaller_product_packagings = product.packaging_ids.filtered(
                lambda p: p.id != packaging.id and packaging.qty > p.qty > 0.0
            )
            res = OrderedDict()
            for p_pack in smaller_product_packagings.sorted(lambda p: p.qty):
                res[p_pack.packaging_type_id.code] = p_pack.qty
            packaging.qty_per_type = packaging._format_qty_per_type(res)

    def _format_qty_per_type(self, qty_per_type_dict):
        self.ensure_one()
        res = []
        for code, qty in qty_per_type_dict.items():
            new_qty = self.qty / qty
            if not new_qty.is_integer():
                new_qty_int = int(new_qty)
                new_qty_decimals = new_qty - new_qty_int
                new_qty = '{}<span style="color: red;">{}</span>'.format(
                    new_qty_int, str(new_qty_decimals).lstrip("0")
                )
            res.append("{} {}".format(new_qty, code))
        return "<div>" + "; ".join(res) + "</div"

    @api.onchange("packaging_type_id")
    def _onchange_name(self):
        if self.packaging_type_id:
            self.name = self.packaging_type_id.name

    @api.depends("name", "packaging_type_id", "packaging_type_id.display_name")
    def _compute_display_name(self):
        return super(ProductPackaging, self)._compute_display_name()

    def name_get(self):
        result = []
        for record in self:
            if record.product_tmpl_id and record.packaging_type_id:
                result.append(
                    (record.id, record.packaging_type_id.display_name)
                )
            else:
                result.append((record.id, record.name))
        return result
