from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _order = 'default_code, id'

    default_code = fields.Char(index=True)
