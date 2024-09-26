from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    id_numbers_ids = fields.One2many(
        "product.identification", "product_id", string="Identification Numbers"
    )
