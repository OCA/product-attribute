# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP / Odoo, Open Source Management Solution - module extension
#    Copyright (C) 2015- O4SB (<http://openforsmallbusiness.co.nz>).
#    Author Graeme Gellatly <g@o4sb.com>
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product Attribute Group',
    'version': '0.1',
    'category': 'Product',
    'summary': 'Allows grouping of attribute values for easy recall',
    'author': 'Roofing Industries, O4SB, Graeme Gellatly, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': [
        'views/product_attribute_group_view.xml',
        'views/product_template_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/product_attribute_group_demo.xml'
    ],
    'installable': True,
}
