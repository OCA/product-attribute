# Copyright 2018 Carlos Dauden - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    _rec_names_search = ["name"]  # Initialize here to be able to extend

    name = fields.Char(store=True)

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

    def _auto_init(self):
        other_fields = ["categ_id", "product_tmpl_id", "product_id"]
        self.env["product.pricelist.item"]._rec_names_search.extend(other_fields)
        return super()._auto_init()

    @api.depends("fixed_price", "previous_item_id.fixed_price")
    def _compute_variation_percent(self):
        for line in self:
            if not (line.fixed_price and line.previous_price):
                line.variation_percent = 0.0
            else:
                line.variation_percent = (
                    line.fixed_price / line.previous_price - 1
                ) * 100
