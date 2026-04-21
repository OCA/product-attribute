# Copyright 2024 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.readonly.security.mixin"]
