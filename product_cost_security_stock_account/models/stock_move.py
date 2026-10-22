# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        # Cache standard price value accessed in svl creation.
        self.product_id.with_company(self.company_id).sudo().read(["standard_price"])
        self.product_id.sudo().read(["standard_price"])
        return super()._action_done(cancel_backorder=cancel_backorder)
