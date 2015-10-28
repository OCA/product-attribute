# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of product_brand_sequence,
#     an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     product_brand_sequence is free software:
#     you can redistribute it and/or modify it under the terms of the GNU
#     Affero General Public License as published by the Free Software
#     Foundation,either version 3 of the License, or (at your option) any
#     later version.
#
#     product_brand_sequence is distributed
#     in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#     even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with product_brand_sequence.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
    cr.execute("UPDATE product_brand "
               "SET code = '!!mig!!' || id "
               "WHERE code IS NULL OR code = '/';")


class ProductBrand(models.Model):
    _inherit = 'product.brand'

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
        return self.env['ir.sequence'].get('product.brand')

    @api.model
    def create(self, vals):
        if 'code' not in vals or vals['code'] == '/':
            vals['code'] = self._get_next_code()
        return super(ProductBrand, self).create(vals)

    @api.multi
    def write(self, vals):
        for this in self:
            v = vals.copy()
            code = v.setdefault('code', this.code)
            if code in [False, '/']:
                v['code'] = self._get_next_code()
            super(ProductBrand, this).write(v)
        return True

    @api.one
    def copy(self, default=None):
        default = default or {}
        default.setdefault('code', self.code + _('-copy'))
        return super(ProductBrand, self).copy(default)
