# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def check_field_access_rights(self, operation, fields):
        override_cost_security = (
            self.env.context.get("pos_override_cost_security")
            and self.env.user.has_group("point_of_sale.group_pos_user")
            and not self.env.user.has_group("product_cost_security.group_product_cost")
            and "standard_price" in fields
        )
        if override_cost_security:
            return super(ProductProduct, self.sudo()).check_field_access_rights(
                operation, fields
            )
        return super().check_field_access_rights(operation, fields)
