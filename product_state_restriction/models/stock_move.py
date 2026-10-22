# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        for move in self:
            state = move.product_id.product_tmpl_id.product_state_id
            if not (state and state.restrict_outgoing):
                continue

            # Only block real outgoing movements
            if move.location_dest_id.usage in (
                "customer",
                "supplier",
                "inventory",
                "production",
            ):
                raise UserError(
                    self.env._(
                        "Product '%(product)s' is in state '%(state)s' and cannot"
                        " leave the warehouse.",
                        product=move.product_id.display_name,
                        state=state.name,
                    )
                )
        return super()._action_done(cancel_backorder=cancel_backorder)
