# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("multi_price", "Other Price")],
        ondelete={"multi_price": "set default"},
    )
    multi_price_name = fields.Many2one(
        comodel_name="product.multi.price.name",
        string="Other Price Name",
    )

    def _compute_price(self, product, quantity, uom, date, currency=None):
        result = super()._compute_price(product, quantity, uom, date, currency)
        is_reprice = self.env.context.get("is_reprice", False)
        if (
            self.compute_price == "formula"
            and self.base == "multi_price"
            and not is_reprice
        ):
            result = product.sudo()._get_multiprice_pricelist_price(self)
        return result
