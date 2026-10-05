# Copyright 2026 360ERP (<https://www.360erp.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductCostSecurityMixin(models.AbstractModel):
    _inherit = "product.cost.security.mixin"

    def _get_module_list_check_cost_security(self):
        return super()._get_module_list_check_cost_security() + [
            "product_cost_security_purchase"
        ]
