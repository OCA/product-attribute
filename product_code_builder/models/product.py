# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2015 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Abdessamad HILALI <abdessamad.hilali@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    base_code = fields.Char(
        'Base Code',
        help="this field is used like a base to automatically create "
             "Internal Reference (default_code)")
    auto_default_code = fields.Boolean('Auto Generate Reference',
                                       default=True)


class ProductProduct(models.Model):
    _inherit = "product.product"

    manual_default_code = fields.Char(
        help="This is an invisible field used to store default_code value"
    )
    default_code = fields.Char(compute="_compute_default_code",
                               inverse="_set_manual_default_code",
                               store=True)

    @api.multi
    def _get_default_code(self):
        """ this method used to create a list of code elements  """
        self.ensure_one()
        res = self.base_code or ''
        for value in self.attribute_value_ids:
            res += ''.join([
                value.attribute_id.code or '',
                value.code or ''
                ])
        return res

    def _set_manual_default_code(self):
        self.manual_default_code = self.default_code

    @api.depends('auto_default_code',
                 'attribute_value_ids.attribute_id.code',
                 'attribute_value_ids.code',
                 'product_tmpl_id.base_code'
                 )
    @api.one
    def _compute_default_code(self):
        if self.auto_default_code:
            self.default_code = self._get_default_code()
        else:
            self.default_code = self.manual_default_code
