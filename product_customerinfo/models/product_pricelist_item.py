# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("partner", "Partner Prices on the product form")],
        ondelete={"partner": "set default"},
    )

    def _compute_price(self, product, quantity, uom, **kwargs):
        return super()._compute_price(
            product.with_context(include_customerinfo_discount=True),
            quantity,
            uom,
            **kwargs,
        )

    @api.onchange("base")
    def _onchange_base_clear_pricelist(self):
        # Only the "pricelist" base uses the pricelist: do not keep a stale one
        if self.base != "pricelist":
            self.base_pricelist_id = False

    @api.onchange("base_pricelist_id")
    def _onchange_base_pricelist_id(self):
        # Core would set the base back to sales price when the pricelist is cleared
        if self.base == "partner":
            return None
        return super()._onchange_base_pricelist_id()

    def _get_price_label_base_str(self):
        if self.base == "partner":
            return self.env._("customer prices")
        return super()._get_price_label_base_str()

    def _show_discount(self):
        # Show discount when pricelist item is based on customerinfo price
        res = super()._show_discount()
        if (
            self
            and self._is_discount_feature_enabled()
            and self.compute_price in ("discount", "markup")
            and self.base == "partner"
        ):
            return True
        return res
