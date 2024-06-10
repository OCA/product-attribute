# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def _get_lot_sequence(self):
        seq_policy = self.env["stock.lot"]._get_sequence_policy()
        if (
            seq_policy == "product"
            and self.product_id
            and self.product_id.product_tmpl_id.lot_sequence_id
        ):
            return self.product_id.product_tmpl_id.lot_sequence_id._next()
        return super()._get_lot_sequence()
