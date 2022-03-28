from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _order = "priority desc, default_code"

    default_code = fields.Char(index=True)
