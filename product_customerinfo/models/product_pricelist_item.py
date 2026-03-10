# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("partner", "Partner Prices on the product form")],
        ondelete={"partner": "set default"},
    )

    def _compute_price(self, product, quantity, uom, date, currency=None, **kwargs):
        return super()._compute_price(
            product.with_context(include_customerinfo_discount=True),
            quantity,
            uom,
            date,
            currency,
            **kwargs,
        )

    def _show_discount(self):
        # Show discount when pricelist item is based on customerinfo price
        res = super()._show_discount()
        if (
            self
            and self._is_discount_feature_enabled()
            and self.compute_price == "formula"
            and self.base == "partner"
        ):
            return True
        return res
