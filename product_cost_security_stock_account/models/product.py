# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_out_svl_vals(self, quantity, company, lot=False):
        # Cache standard price value accessed for svls.
        self.sudo().read(["standard_price"])
        return super()._prepare_out_svl_vals(quantity, company, lot=lot)

    def _prepare_in_svl_vals(self, quantity, unit_cost, lot=False):
        # Cache standard price value accessed for svls.
        self.sudo().read(["standard_price"])
        return super()._prepare_in_svl_vals(quantity, unit_cost, lot=lot)
