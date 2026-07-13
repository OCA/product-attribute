# Copyright 2026 Tecnativa - Carlos Roca
# Copyright 2026 Kreilabs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models
from odoo.addons.stock_account.models.product import ProductProduct as StockAccountProductProduct

_VALUATION_CTX = {"_product_cost_security_valuation": True}


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_cost = fields.Monetary(groups="product_cost_security.group_product_cost")
    total_value = fields.Monetary(groups="product_cost_security.group_product_cost")

    def _with_product_cost_valuation(self):
        """Return self with internal cost-read ACL bypass for valuation flows."""
        return self.with_context(**_VALUATION_CTX)

    def _product_cost_fields_for_valuation_cache(self):
        """Field names to pre-cache before internal valuation reads."""
        fields_to_cache = ["standard_price"]
        if "fc_standard_price" in self._fields:
            fields_to_cache.append("fc_standard_price")
        return fields_to_cache

    def _cache_standard_price_for_valuation(self):
        """Pre-cache cost for internal stock valuation flows."""
        fields_to_cache = self._product_cost_fields_for_valuation_cache()
        self.sudo().read(fields_to_cache)
        lots = self.env["stock.lot"].search([("product_id", "in", self.ids)])
        if lots:
            lot_fields = [fname for fname in fields_to_cache if fname in lots._fields]
            lots.sudo().read(lot_fields)

    @api.model_create_multi
    def create(self, vals_list):
        """Create products without reading standard_price before valuation ACL bypass.

        stock_account.create evaluates ``product.standard_price`` in a
        comprehension before any ACL bypass; users without the cost group get
        AccessError even when the value is 0. Skip that body and revaluate
        safely with the valuation context.
        """
        products = super(StockAccountProductProduct, self).create(vals_list)
        products_val = products._with_product_cost_valuation()
        products_val._cache_standard_price_for_valuation()
        to_revalue = products_val.filtered(lambda product: product.standard_price)
        if to_revalue:
            to_revalue.with_context(
                valuation_date=datetime.min
            )._change_standard_price({product: 0 for product in to_revalue})
        return products

    def write(self, vals):
        if "standard_price" in vals and not self.env.context.get(
            "disable_auto_revaluation"
        ):
            self = self._with_product_cost_valuation()
            self._cache_standard_price_for_valuation()
        return super().write(vals)

    def _change_standard_price(self, old_price):
        self = self._with_product_cost_valuation()
        self._cache_standard_price_for_valuation()
        return super()._change_standard_price(old_price)

    def _update_standard_price(self, extra_value=None, extra_quantity=None):
        self = self._with_product_cost_valuation()
        self._cache_standard_price_for_valuation()
        return super()._update_standard_price(
            extra_value=extra_value, extra_quantity=extra_quantity
        )
