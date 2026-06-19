# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_cost = fields.Monetary(groups="product_cost_security.group_product_cost")
    total_value = fields.Monetary(groups="product_cost_security.group_product_cost")

    def _cache_standard_price_for_valuation(self):
        """Pre-cache cost for internal stock valuation flows."""
        self.sudo().read(["standard_price"])
        lots = self.env["stock.lot"].search([("product_id", "in", self.ids)])
        if lots:
            lots.sudo().read(["standard_price"])

    def _change_standard_price(self, old_price):
        self._cache_standard_price_for_valuation()
        return super()._change_standard_price(old_price)

    def _update_standard_price(self, extra_value=None, extra_quantity=None):
        self._cache_standard_price_for_valuation()
        return super()._update_standard_price(
            extra_value=extra_value, extra_quantity=extra_quantity
        )
