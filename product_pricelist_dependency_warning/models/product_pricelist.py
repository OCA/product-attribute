#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_base_price_changed = fields.Boolean(
        compute="_compute_is_base_price_changed",
        store=True,
        string="Base price changed",
        help="The base price of some price rules is changed.",
    )

    @api.depends(
        "item_ids.is_base_price_changed",
    )
    def _compute_is_base_price_changed(self):
        for pricelist in self:
            lines_base_price_changed = pricelist.item_ids.mapped(
                "is_base_price_changed"
            )
            pricelist.is_base_price_changed = any(lines_base_price_changed)
