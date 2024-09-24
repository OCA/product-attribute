from odoo import fields, models


class ProductIdCategory(models.Model):
    _name = "product.product.id_category"
    _description = "Product Identification Category"

    name = fields.Char(required=True)
