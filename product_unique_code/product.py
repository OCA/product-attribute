from openerp import models, fields, api

class ProductUniqueCode(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(required=True)

    _sql_constraints = [
        ('unique_default_code',
         'unique(default_code)',
         'The code must be unique'),
    ]

    @api.one
    def copy(self, default=None):
        new_code = self.default_code + '-2'
        return super(ProductUniqueCode, self).copy({'default_code': new_code})
