# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def read(self, fields=None, load="_classic_read"):
        """Make an exception when loading data to PoS"""
        if self.env.context.get(
            "pos_override_cost_security"
        ) and self.env.user.has_group("point_of_sale.group_pos_user"):
            fields = fields if fields else []
            other_fields = [f for f in fields if f != "standard_price"]
            self.check_field_access_rights("read", other_fields)
            return super(ProductProduct, self.sudo()).read(fields=fields, load=load)
        return super().read(fields=fields, load=load)
