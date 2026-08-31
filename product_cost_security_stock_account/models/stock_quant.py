# Copyright 2026 Kreilabs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

_VALUATION_CTX = {"_product_cost_security_valuation": True}


class StockQuant(models.Model):
    _inherit = "stock.quant"

    value = fields.Monetary(
        groups="product_cost_security.group_product_cost",
        compute_sudo=True,
    )

    def _compute_value(self):
        """Read product/lot total_value without granting cost ACL to stock users."""
        self = self.with_context(**_VALUATION_CTX)
        return super()._compute_value()
