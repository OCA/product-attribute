from odoo import fields, models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    is_favorite = fields.Boolean(
        related="attribute_id.is_favorite",
    )
