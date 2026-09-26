# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def action_generate_lot_line_vals(self, context, mode, first_lot, count, lot_text):
        # populate the serial generate dialog default value
        if mode == "generate" and not first_lot:
            product = self.env["product.product"].browse(
                context.get("default_product_id")
            )
            first_lot = self.env["stock.lot"]._propose_next_name(product)
        return super().action_generate_lot_line_vals(
            context, mode, first_lot, count, lot_text
        )
