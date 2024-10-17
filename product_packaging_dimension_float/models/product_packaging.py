from odoo import fields, models


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    height = fields.Float()
    width = fields.Float()
    packaging_length = fields.Float()
