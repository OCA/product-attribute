# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _name = "product.supplierinfo"
    _inherit = ["product.supplierinfo", "product.cost.security.mixin"]

    # Inherited fields
    price = fields.Float(groups="product_cost_security.group_product_cost")
