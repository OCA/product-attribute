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
        ondelete="set null",
    )

    def _compute_price(self, product, quantity, uom, date, currency=None, **kwargs):
        # Recompute price after calling the atomic super method for
        # getting proper prices when based on multi price. Extra keyword
        # arguments (e.g. ``task_id`` from the field service product catalog)
        # are passed on, as the core signature accepts them.
        price = super()._compute_price(
            product, quantity, uom, date, currency=currency, **kwargs
        )
        if self.compute_price == "formula" and self.base == "multi_price":
            price = product._get_multiprice_pricelist_price(self)
        return price
