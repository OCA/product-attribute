# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_type = fields.Selection(required=True, selection=[
        ('select', 'Select'),
        ('range', 'Range'),
        ('numeric', 'Numeric')], string="Type", default='select')


class ProductAttributeLine(models.Model):
    _inherit = "product.attribute.line"

    required = fields.Boolean('Required')
    default = fields.Many2one('product.attribute.value', 'Default')
    attr_type = fields.Selection(string='Type', store=False,
                                 related='attribute_id.attr_type')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_type = fields.Selection(string='Type',
                                 related='attribute_id.attr_type')
    numeric_value = fields.Float('Numeric Value',
                                 digits=dp.get_precision('Product Attribute'))
    min_range = fields.Float('Min',
                             digits=dp.get_precision('Product Attribute'))
    max_range = fields.Float('Max',
                             digits=dp.get_precision('Product Attribute'))

    @api.constrains('min_range', 'max_range')
    def _check_min_max_range(self):
        for value in self:
            # we check only values of range type attributes.
            if value.attr_type != 'range':
                continue
            if value.min_range > value.max_range:
                raise exceptions.Warning(
                    _('The min range should be less than the max range.'))
        return True
