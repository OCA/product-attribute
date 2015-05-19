# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2015 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Benoît GUILLOT <benoit.guillot@akretion.com>
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

from openerp import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    code = fields.Char('Code')
    sequence = fields.Integer('Sequence')
    _sql_constraints = [
        ('attr_code_uniq', 'unique(code)',
         "With each Attribute we must be found a unique 'code'"),
    ]


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char('Code')
    comment = fields.Text('Comment')
    readonly = fields.Boolean(
        help="This is an invisible field it allows us to control code and"
        "comment fields")
    _sql_constraints = [
        ('attr_val_code_uniq', 'unique(code, attribute_id)',
         "With each Attribute we must be found a unique 'code'"),
        ]
