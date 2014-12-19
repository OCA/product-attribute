from openerp import models, fields, api


class ProductUniqueCode(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(copy=False)

    _sql_constraints = [
        ('unique_default_code',
         'unique(default_code)',
         'The code must be unique'),
    ]
