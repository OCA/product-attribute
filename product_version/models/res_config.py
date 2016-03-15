# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class ProductConfigSettings(models.TransientModel):
    _name = 'product.config.settings'
    _inherit = 'res.config.settings'

    group_product_version = fields.Boolean(
        string='Allow to re-edit Products',
        implied_group='product_version.group_product_version',
        help='The active state may be passed back to state draft')
    active_product_draft = fields.Boolean(
        string='Keep re-editing Product active',
        help='This will allow you to define if those Product passed back to '
        'draft are still activated or not')

    def _get_parameter(self, key, default=False):
        param_obj = self.env['ir.config_parameter']
        rec = param_obj.search([('key', '=', key)])
        return rec or default

    def _write_or_create_param(self, key, value):
        param_obj = self.env['ir.config_parameter']
        rec = self._get_parameter(key)
        if rec:
            if not value:
                rec.unlink()
            else:
                rec.value = value
        elif value:
            param_obj.create({'key': key, 'value': value})

    @api.multi
    def get_default_parameters(self):
        def get_value(key, default=''):
            rec = self._get_parameter(key)
            return rec and rec.value or default
        return {
            'active_product_draft': get_value('active.product.draft', False),
        }

    @api.multi
    def set_parameters(self):
        self._write_or_create_param(
            'active.product.draft', self.active_product_draft)
