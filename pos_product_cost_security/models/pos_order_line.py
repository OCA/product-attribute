# Copyright 2026 INVITU
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    margin = fields.Monetary(groups="product_cost_security.group_product_cost")
    margin_percent = fields.Float(groups="product_cost_security.group_product_cost")
    total_cost = fields.Float(groups="product_cost_security.group_product_cost")

    def _compute_total_cost(self, stock_moves):
        return super(PosOrderLine, self.sudo())._compute_total_cost(stock_moves)
