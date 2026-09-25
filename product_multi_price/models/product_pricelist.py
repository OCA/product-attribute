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

    def _compute_base_price(self, product, quantity, uom, date, target_currency):
        """A multi price base comes from the price name of the rule, which
        price_compute() does not know, in the unit and currency asked for."""
        if self.base != "multi_price" or self.env.context.get("is_reprice", False):
            return super()._compute_base_price(
                product, quantity, uom, date, target_currency
            )
        target_currency.ensure_one()
        price = product.sudo()._get_multiprice_base_price(self, date)
        if uom and uom != product.uom_id:
            price = product.uom_id._compute_price(price, uom)
        if product.currency_id != target_currency:
            price = product.currency_id._convert(
                price, target_currency, self.env.company, date, round=False
            )
        return price
