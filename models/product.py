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

    default_code = fields.Char(string='Internal Reference')
    template_default_code = fields.Char(string='Template Internal Reference')

    @api.one
    def write(self, vals):
        product_obj = self.env['product.product']
        result = super(ProductTemplate, self).write(vals)
        if 'template_default_code' in vals:
            cond = [('product_tmpl_id', '=', self.id)]
            products = product_obj.search(cond)
            for product in products:
                my_code = False
                for attribute_value in product.attribute_value_ids:
                    if not my_code:
                        my_code = attribute_value.attribute_code
                    else:
                        my_code += '/' + attribute_value.attribute_code
                default_code = self.template_default_code
                if my_code:
                    default_code += ' - ' + my_code
                product.default_code = default_code
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        product_tmpl_id = values.get('product_tmpl_id', False)
        attribute_value_ids = values.get('attribute_value_ids', False)
        product = super(ProductProduct, self).create(values)
        if product_tmpl_id and attribute_value_ids:
            my_code = False
            for attribute_value in product.attribute_value_ids:
                if not my_code:
                    my_code = attribute_value.attribute_code
                else:
                    my_code += '/' + attribute_value.attribute_code
            default_code = product.template_default_code
            if my_code:
                default_code += ' - ' + my_code
            product.default_code = default_code
        return product


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.attribute_code = self.name[0:1]

    attribute_code = fields.Char(string='Attribute Code', required=True,
                                 default=onchange_name)
