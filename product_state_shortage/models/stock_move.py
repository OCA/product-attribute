# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder=cancel_backorder)

        done_incoming_moves = self.filtered(
            lambda m: m.picking_code == "incoming" and m.state == "done"
        )
        if not done_incoming_moves:
            return res

        shortage_products = self.env["product.product"].search(
            [
                ("id", "in", done_incoming_moves.product_id.ids),
                ("product_state_id.is_shortage", "=", True),
            ]
        )
        if shortage_products:
            shortage_products.product_tmpl_id._reset_default_state()

        return res
