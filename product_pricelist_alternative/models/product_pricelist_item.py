# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    @api.constrains("base")
    def _check_pricelist_alternative_items_based_on_other_pricelist(self):
        """Alternative pricelists can not contain items based on other pricelist"""
        for item in self:
            if (
                item.compute_price == "formula"
                and item.base == "pricelist"
                and item.pricelist_id.is_alternative_to_pricelist_count
            ):
                raise ValidationError(
                    _(
                        "It is not possible to encode this price rule. Formulas based "
                        "on another pricelist are not allowed on alternative pricelists."
                        " Please change to another type of price computation."
                    )
                )
