# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# © 2015 Domatix (http://domatix.com)
# Angel Moua <angel.moya@domatix.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api
from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prefix_code = fields.Char(
        required=True,
        default='/')

    @api.model
    def create(self, vals):
        if 'prefix_code' not in vals or vals['prefix_code'] == '/':
            vals['prefix_code'] = self.env['ir.sequence'].get(
                'product.product')
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('prefix_code') in [False, '/']:
            for product in self:
                vals['prefix_code'] = self.env['ir.sequence'].get(
                    'product.product')
                super(ProductTemplate, product).write(vals)
        else:
            super(ProductTemplate, self).write(vals)
        return True

    @api.multi
    def copy(self, default=None):
        for product in self:
            if default is None:
                default = {}
            if product.prefix_code:
                default.update({
                    'prefix_code': self.prefix_code + _('-copy'),
                })
        return super(ProductTemplate, self).copy(default)
