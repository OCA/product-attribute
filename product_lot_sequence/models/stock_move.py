# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        """Avoid calling and incrementing the sequence if not needed or already done"""
        seq_policy = self.env["stock.lot"]._get_sequence_policy()

        if seq_policy in ("product", "global"):
            # If move is not supposed to assign serial pass empty string for next serial
            if not self.display_assign_serial:
                self = self.with_context(force_next_serial="")
            # If the sequence was already called once, avoid calling it another time
            elif self.next_serial:
                self = self.with_context(force_next_serial=self.next_serial)
            elif self.product_id.tracking == "serial" and self.state == "assigned":
                self.next_serial = self.env["stock.lot"]._get_next_serial(
                    self.company_id, self.product_id
                )
        return super().action_show_details()

    @api.model
    def action_generate_lot_line_vals(self, context, mode, first_lot, count, lot_text):
        # populate the serial generate dialog default value
        if mode == "generate" and not first_lot:
            product = self.env["product.product"].browse(
                context.get("default_product_id")
            )
            first_lot = self.env["stock.lot"]._get_next_serial(
                self.env.company, product
            )
        return super().action_generate_lot_line_vals(
            context, mode, first_lot, count, lot_text
        )
