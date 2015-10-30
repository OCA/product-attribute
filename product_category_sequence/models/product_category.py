# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.translate import _


def update_null_and_slash_codes(cr):  # pragma: no cover
    """
    Updates existing codes matching the default '/' or
    empty. Primarily this ensures installation does not
    fail for demo data.
    :param cr: database cursor
    :return: void
    """
    cr.execute("UPDATE product_category "
               "SET code = '!!mig!!' || id "
               "WHERE code IS NULL OR code = '/';")


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code = fields.Char(
        required=True,
        default='/'
        )

    _sql_constraints = [
        ('uniq_code',
         'unique(code)',
         'The reference must be unique'),
    ]

    @api.model
    def _get_next_code(self):
        return self.env['ir.sequence'].get('product.category')

    @api.model
    def create(self, vals):
        if 'code' not in vals or vals['code'] == '/':
            vals['code'] = self._get_next_code()
        return super(ProductCategory, self).create(vals)

    @api.multi
    def write(self, vals):
        for this in self:
            v = vals.copy()
            code = v.setdefault('code', this.code)
            if code in [False, '/']:
                v['code'] = self._get_next_code()
            super(ProductCategory, this).write(v)
        return True

    @api.one
    def copy(self, default=None):
        default = default or {}
        default.setdefault('code', self.code + _('-copy'))
        return super(ProductCategory, self).copy(default)
