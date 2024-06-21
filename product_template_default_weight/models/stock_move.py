# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _cal_move_weight(self):
        res = super()._cal_move_weight()

        for move in self:
            total_weight = 0
            if move.product_id.weight:
                total_weight += move.product_id.weight * move.product_qty
            else:
                total_weight += (
                    move.product_id.product_tmpl_id.weight * move.product_qty
                )
            move.weight = total_weight
        return res
