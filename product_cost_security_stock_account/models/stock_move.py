# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _cache_product_cost_for_valuation(self):
        products = self.product_id.with_company(self.company_id)
        products.sudo().read(["standard_price"])
        lots = self.move_line_ids.lot_id
        if lots:
            lots.sudo().read(["standard_price"])

    def _action_done(self, cancel_backorder=False):
        self._cache_product_cost_for_valuation()
        return super()._action_done(cancel_backorder=cancel_backorder)
