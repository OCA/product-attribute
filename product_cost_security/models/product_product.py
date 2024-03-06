# Copyright 2018 Sergio Teruel - Tecnativa <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.cost.security.mixin"]

    # Inherited fields
    standard_price = fields.Float(groups="product_cost_security.group_product_cost")
