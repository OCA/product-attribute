from odoo import fields, models


class ProductIdentificationCategory(models.Model):
    _name = "product.identification.category"
    _description = "Product Identification Category"

    name = fields.Char(required=True)
