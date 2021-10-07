# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        """We don't need to recompute the whole string we just set the last char on as
        it is the only possible truth. The cron well be in charge of reseting them every
        week anyway."""
        moves_todo = super()._action_done(cancel_backorder=cancel_backorder)
        products = (
            moves_todo.filtered(
                lambda x: x.sale_line_id and x.picking_code == "outgoing"
            )
            .mapped("product_id")
            .with_context(force_company=self.company_id.id)
        )
        for product in products.filtered(lambda x: x.weekly_sold_delivered[-1:] == "0"):
            product.weekly_sold_delivered = product.weekly_sold_delivered[:-1] + "1"
        return moves_todo
