# Copyright 2018 Carlos Dauden - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    name = fields.Char(search="_search_name")

    previous_item_id = fields.Many2one(
        comodel_name="product.pricelist.item",
        string="Previous Item",
        help="Relation with previous item when duplicate line",
    )
    previous_price = fields.Float(
        related="previous_item_id.fixed_price", string="Previous Fixed Price"
    )
    variation_percent = fields.Float(
        compute="_compute_variation_percent",
        store=True,
        digits="Product Price",
        string="Variation %",
    )

    @api.model
    def _search_name(self, operator, value):
        return [
            "|",
            "|",
            ("categ_id", operator, value),
            ("product_tmpl_id", operator, value),
            ("product_id", operator, value),
        ]

    @api.depends("fixed_price", "previous_item_id.fixed_price")
    def _compute_variation_percent(self):
        for line in self:
            if not (line.fixed_price and line.previous_price):
                line.variation_percent = 0.0
            else:
                line.variation_percent = (
                    line.fixed_price / line.previous_price - 1
                ) * 100
