from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    description = fields.Text(translate=True)
