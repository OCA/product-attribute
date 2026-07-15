# Copyright 2026 Tecnativa - Carlos Roca
# Copyright 2026 Kreilabs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

_VALUATION_CTX = {"_product_cost_security_valuation": True}


class StockMove(models.Model):
    _inherit = "stock.move"

    def _cache_product_cost_for_valuation(self):
        """Pre-cache product/lot costs (and FC cost when present) for valuation."""
        products = self.product_id.with_company(self.company_id)
        fields_to_cache = ["standard_price"]
        if "fc_standard_price" in products._fields:
            fields_to_cache.append("fc_standard_price")
        products.sudo().read(fields_to_cache)
        lots = self.move_line_ids.lot_id
        if lots:
            lot_fields = [fname for fname in fields_to_cache if fname in lots._fields]
            lots.sudo().read(lot_fields)

    def _action_done(self, cancel_backorder=False):
        # Context flag is required in Odoo 19: field ACL is checked on every
        # attribute get, so sudo().read alone no longer unlocks standard_price.
        self = self.with_context(**_VALUATION_CTX)
        self._cache_product_cost_for_valuation()
        return super()._action_done(cancel_backorder=cancel_backorder)
