# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    alternative_pricelist_policy = fields.Selection(
        selection=[
            ("use_lower_price", "Use lower price"),
            ("ignore", "Ignore alternatives"),
        ],
        default="use_lower_price",
        required=True,
    )
