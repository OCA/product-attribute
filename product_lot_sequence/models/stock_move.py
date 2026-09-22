# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        # propose the next serial of the sequence
        self.ensure_one()
        lot_model = self.env["stock.lot"]
        if (
            self.display_assign_serial
            and self.product_id.tracking == "serial"
            and self.state == "assigned"
            # if the name is not yet consumed, can peek a fresh one
            and (lot_model._consume_on_create() or not self.next_serial)
        ):
            self.next_serial = lot_model._propose_next_name(self.product_id)
        return super().action_show_details()

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
