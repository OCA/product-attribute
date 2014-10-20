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

from openerp.osv import orm, fields


class ProductAttribute(orm.Model):
    _inherit = "product.attribute"

    _columns = {
        'type': fields.selection([
            ('radio', 'Radio'),
            ('select', 'Select'),
            ('color', 'Color'),
            ('hidden', 'Hidden'),
            ('range', 'Range'),
            ('numeric', 'Numeric'),
            ('custom', 'Custom')], string="Type", type="char"),
    }


class ProductAttributeLine(orm.Model):
    _inherit = "product.attribute.line"

    _columns = {
        'required': fields.boolean('Required'),
        'default': fields.many2one('product.attribute.value', 'Default'),
        'attr_type': fields.related('attribute_id', 'type', type='char',
                                    string='Type', store=True),
    }


class ProductAttributeValue(orm.Model):
    _inherit = "product.attribute.value"

    _columns = {
        'attr_type': fields.related('attribute_id', 'type', type='char',
                                    string='Type', store=False),
        'custom_value': fields.char('Custom Value', size=128),
        'numeric_value': fields.float('Numeric Value', digits=(12, 6)),
        'min_range': fields.float('Min', digits=(12, 6)),
        'max_range': fields.float('Max', digits=(12, 6)),
    }
