# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    product_lot_sequence_id = fields.Many2one(
        "product.lot.sequence",
        domain="['|',('product_id','=', product_id),"
        "'&',('product_id','=', False),('product_tmpl_id','=', product_tmpl_id)]",
    )
    available_product_lot_sequence_ids = fields.Many2many(
        "product.lot.sequence", compute="_compute_available_product_lot_sequence_ids"
    )
    available_product_lot_sequence_count = fields.Integer(
        compute="_compute_available_product_lot_sequence_ids"
    )
    product_tmpl_id = fields.Many2one(
        "product.template", related="product_id.product_tmpl_id"
    )

    @api.depends("product_id")
    def _compute_available_product_lot_sequence_ids(self):
        for rec in self:
            if rec.product_id:
                pls_ids = rec.product_id.product_tmpl_id.product_lot_sequence_ids
                available = pls_ids.filtered(lambda x: x.product_id == self.product_id)
                if not available:
                    available = pls_ids.filtered(
                        lambda x: x.product_id.product_tmpl_id == self.product_tmpl_id
                    )
                rec.available_product_lot_sequence_ids = available
                rec.available_product_lot_sequence_count = len(available)

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            if len(self.available_product_lot_sequence_ids) == 1:
                self.product_lot_sequence_id = self.available_product_lot_sequence_ids[
                    0
                ]

    @api.onchange("product_lot_sequence_id")
    def onchange_product_lot_sequence_id(self):
        if self.product_lot_sequence_id:
            self.name = self.product_lot_sequence_id.lot_sequence_id.get_next_char(
                self.product_lot_sequence_id.lot_sequence_id.number_next_actual
            )

    @api.multi
    def write(self, vals):
        for _ in self:
            if vals.get("product_lot_sequence_id", False):
                pls = self.env["product.lot.sequence"].browse(
                    vals.get("product_lot_sequence_id", False)
                )
                if vals.get("name", False) != pls.lot_sequence_id.get_next_char(
                    pls.lot_sequence_id.number_next_actual
                ):
                    vals["name"] = pls.lot_sequence_id._next()
                else:
                    pls.lot_sequence_id._next()
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get("product_lot_sequence_id", False):
            pls = self.env["product.lot.sequence"].browse(
                vals.get("product_lot_sequence_id", False)
            )
            if vals.get("name", False) != pls.lot_sequence_id.get_next_char(
                pls.lot_sequence_id.number_next_actual
            ):
                vals["name"] = pls.lot_sequence_id._next()
            else:
                pls.lot_sequence_id._next()
        return super().create(vals)
