# -*- coding: utf-8 -*-
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

from openerp import models, fields


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _order = 'priority, name'

    priority = fields.Integer(
        string='Priority',
        help='Define priority of exhibition in reports',
        default=10,
    )


class ProductAttributeValue(models.Model):

    _inherit = 'product.attribute.value'
    _order = 'priority, name'

    priority = fields.Integer(
        string='Priority',
        readonly=True,
        store=True,
        related='attribute_id.priority',
        help='Define priority of exhibition in reports'
    )


class ProductAttributeLine(models.Model):

    _inherit = 'product.attribute.line'
    _order = 'priority'

    priority = fields.Integer(
        string='Priority',
        readonly=True,
        store=True,
        related='value_ids.priority',
        help='Define priority of exhibition in reports'
    )
