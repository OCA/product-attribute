from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "default_code, id"
