# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _cal_move_weight(self):
        # full overload of the original method to use
        # product_tmpl_id.weight if product_id.weight is 0.00
        moves_with_weight = self.filtered(
            lambda m: m.product_id.weight > 0.00
            or m.product_id.product_tmpl_id.weight > 0.00
        )
        for move in moves_with_weight:
            weight = move.product_id.weight or move.product_id.product_tmpl_id.weight
            move.weight = move.product_qty * weight
        (self - moves_with_weight).weight = 0
