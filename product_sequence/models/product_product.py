# -*- coding: utf-8 -*-
# © 2004 Tiny SPRL
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


def update_null_and_slash_codes(cr):  # pragma: no cover
    """
    Updates existing codes matching the default '/' or
    empty. Primarily this ensures installation does not
    fail for demo data.
    :param cr: database cursor
    :return: void
    """
    cr.execute("UPDATE product_product "
               "SET default_code = '!!mig!!' || id "
               "WHERE default_code IS NULL OR default_code = '/';")


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
            vals['default_code'] = self.env['ir.sequence'].get(
                'product.product')
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        for product in self:
            if product.default_code in [False, '/']:
                vals['default_code'] = self.env['ir.sequence'].get(
                    'product.product')
            super(ProductProduct, product).write(vals)
        return True

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        if self.default_code:
            default.update({
                'default_code': self.default_code + _('-copy'),
            })
        return super(ProductProduct, self).copy(default)
