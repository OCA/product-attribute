# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    previous_info_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Previous info",
        help="Relation with previous info when duplicate line",
    )
    previous_price = fields.Float(
        related="previous_info_id.price", string="Previous Price"
    )
    variation_percent = fields.Float(
        compute="_compute_variation_percent",
        store=True,
        digits="Product Price",
        string="Variation %",
    )

    @api.depends("price", "previous_info_id.price")
    def _compute_variation_percent(self):
        for line in self:
            if not (line.price and line.previous_price):
                x = line.variation_percent
            else:
                x = (line.price / line.previous_price - 1) * 100
            line.variation_percent = x
