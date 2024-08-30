from odoo import models


class ProductAttribute(models.Model):
    _inherit = ["product.attribute", "product.attribute.favorite.mixin"]
    _name = "product.attribute"
