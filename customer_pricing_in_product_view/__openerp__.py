# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution - module extension
#    Copyright (C) 2014- O4SB (<http://o4sb.com>).
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
    'name': 'Display Customer Price in Product View',
    'version': '1.2.1',
    'category': 'Sales',
    'author': "O4SB - Graeme Gellatly,Odoo Community Association (OCA)",
    'website': 'http://www.o4sb.com',
    'license': 'AGPL-3',
    'depends': ['base', 'product'],
    'description': '''
    This module provides:
        A button on the partner form to show Customer Pricing when
        viewing a list of products.
    ''',
    'data': ['views/res_partner_view.xml'],
    'installable': True,
    'active': True
}
