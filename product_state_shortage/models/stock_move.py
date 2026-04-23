# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder=cancel_backorder)

        incoming_moves = self.filtered(lambda m: m.picking_code == "incoming")
        if incoming_moves:
            shortage_products_to_reset = incoming_moves.product_id.filtered(
                lambda p: p.product_state_id.is_shortage
            )

            if shortage_products_to_reset:
                shortage_products_to_reset.product_tmpl_id._reset_default_state()

        return res
