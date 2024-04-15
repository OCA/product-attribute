# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def read(self, fields=None, load="_classic_read"):
        """Make an exception when loading data to PoS. We load the cost price separetly
        to avoid multi-company issues when doing the call with sudo"""
        fields = fields or []
        override_cost_security = (
            self.env.context.get("pos_override_cost_security")
            and self.env.user.has_group("point_of_sale.group_pos_user")
            and not self.env.user.has_group("product_cost_security.group_product_cost")
            and "standard_price" in fields
        )
        if not override_cost_security:
            return super().read(fields=fields, load=load)
        other_fields = [f for f in fields if f != "standard_price"]
        result = super().read(fields=other_fields, load=load)
        std_price_result = super(ProductProduct, self.sudo()).read(
            fields=["standard_price"], load=load
        )
        # No we zip both results altogether to feed the PoS data load
        for res_item, std_price_res_item in zip(result, std_price_result):
            res_item["standard_price"] = std_price_res_item["standard_price"]
        return result
