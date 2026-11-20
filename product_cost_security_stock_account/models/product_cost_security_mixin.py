from odoo import models


class ProductCostSecurityMixin(models.AbstractModel):
    _inherit = "product.cost.security.mixin"

    def _get_module_list_check_cost_security(self):
        return super()._get_module_list_check_cost_security() + [
            "product_cost_security_stock_account"
        ]
