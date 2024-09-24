from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    id_numbers = fields.One2many(
        "product.product.id_number", "product_id", string="Identification Numbers"
    )
