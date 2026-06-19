# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLot(models.Model):
    _inherit = ["stock.lot", "product.cost.security.mixin"]

    standard_price = fields.Float(groups="product_cost_security.group_product_cost")
    avg_cost = fields.Monetary(groups="product_cost_security.group_product_cost")
    total_value = fields.Monetary(groups="product_cost_security.group_product_cost")
