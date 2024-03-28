# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    cost = fields.Float(
        related="product_tmpl_id.standard_price",
        digits="Product Price",
    )
    margin = fields.Float(
        compute="_compute_margin",
        digits="Product Price",
    )
    margin_percent = fields.Float(
        string="Margin (%)",
        compute="_compute_margin",
    )

    @api.depends("fixed_price", "cost")
    def _compute_margin(self):
        for item in self:
            margin = percentage = 0
            if not float_is_zero(
                item.fixed_price, precision_digits=item.currency_id.rounding
            ):
                margin = item.fixed_price - item.cost
                percentage = (margin / item.fixed_price) * 100
            item.margin = margin
            item.margin_percent = percentage
