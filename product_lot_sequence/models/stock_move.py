# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        """Avoid calling and incrementing the sequence if not needed or already done"""
        seq_policy = self.env["stock.production.lot"]._get_sequence_policy()
        if seq_policy in ("product", "global"):
            # If move is not supposed to assign serial pass empty string for next serial
            if not self.display_assign_serial:
                return super(
                    StockMove, self.with_context(force_next_serial="")
                ).action_show_details()
            # If the sequence was already called once, avoid calling it another time
            elif self.next_serial:
                return super(
                    StockMove, self.with_context(force_next_serial=self.next_serial)
                ).action_show_details()
        return super().action_show_details()
