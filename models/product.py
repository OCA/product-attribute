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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        product_tmpl_id = values.get('product_tmpl_id', False)
        attribute_value_ids = values.get('attribute_value_ids', False)
        product = super(ProductProduct, self).create(values)
        if product_tmpl_id and attribute_value_ids:
            default_code = False
            for attribute_value in product.attribute_value_ids:
                if not default_code:
                    default_code = attribute_value.attribute_code
                else:
                    default_code += '/' + attribute_value.attribute_code
            product.default_code = default_code
        return product


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.model
    def _default_attribute_code(self):
        self.onchange_name()

    attribute_code = fields.Char(string='Attribute Code', required=True,
                                 default=_default_attribute_code)

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.attribute_code = self.name[0:1]
