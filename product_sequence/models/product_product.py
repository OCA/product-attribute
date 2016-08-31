# -*- coding: utf-8 -*-
# © 2004 Tiny SPRL
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(
        string='Reference',
        size=64,
        index=True,
        required=True,
        default='/')

    _sql_constraints = [
        ('uniq_default_code',
         'unique(default_code)',
         'The reference must be unique'),
    ]

    @api.model
    def create(self, vals):
        if 'default_code' not in vals or vals['default_code'] == '/':
            sequence = self.env.ref('product_sequence.seq_product_auto')
            vals['default_code'] = sequence.next_by_id()
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        for product in self:
            if product.default_code in [False, '/']:
                sequence = self.env.ref('product_sequence.seq_product_auto')
                vals['default_code'] = sequence.next_by_id()
            super(ProductProduct, product).write(vals)
        return True

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        if self.default_code:
            default.update({
                'default_code': self.default_code + _('-copy'),
            })
        return super(ProductProduct, self).copy(default)
