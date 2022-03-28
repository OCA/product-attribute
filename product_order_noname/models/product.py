from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "priority desc, default_code, id"
