# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id and self.product_id.product_tmpl_id.lot_sequence_id:
            self.name = self.product_id.product_tmpl_id.lot_sequence_id._next()

    @api.model_create_multi
    def create(self, vals_list):
        for lot_vals in vals_list:
            if "name" not in lot_vals:
                product = self.env["product.product"].browse(lot_vals["product_id"])
                if product and product.product_tmpl_id.lot_sequence_id:
                    lot_vals["name"] = product.product_tmpl_id.lot_sequence_id._next()
        return super(ProductionLot, self).create(vals_list)
