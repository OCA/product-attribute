# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_prefix = fields.Char(
        string='Reference prefix',
        help='Prefix for using when building internal references for the '
             'variants generated from this template')

    @api.one
    def write(self, vals):
        product_obj = self.env['product.product']
        result = super(ProductTemplate, self).write(vals)
        if 'default_prefix' in vals:
            cond = [('product_tmpl_id', '=', self.id)]
            products = product_obj.search(cond)
            for product in products:
                default_code = self.default_prefix or ''
                for value in product.attribute_value_ids:
                    if value.attribute_code:
                        default_code += '/%s' % value.attribute_code
                product.default_code = default_code
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        product = super(ProductProduct, self).create(values)
        default_code = product.default_prefix or ''
        for value in product.attribute_value_ids:
            if value.attribute_code:
                default_code += '/%s' % value.attribute_code
        if default_code:
            product.default_code = default_code
        return product


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.attribute_code = self.name[0:1]

    attribute_code = fields.Char(
        string='Attribute Code', default=onchange_name)

    @api.model
    def create(self, values):
        if 'attribute_code' not in values:
            values['attribute_code'] = values.get('name', '')[0:1]
        value = super(ProductAttributeValue, self).create(values)
        return value
