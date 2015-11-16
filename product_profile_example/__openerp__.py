# coding: utf-8
##############################################################################
#
#    Author: David BEAL
#    Copyright 2015 Akretion
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
    'name': 'Product Profile Example',
    'summary': 'Product Profile Use Case',
    'version': '0.3',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'maintainer': 'Akretion',
    'category': 'product',
    'description': 'See Product Profile module',
    'depends': [
        'product_profile',
        'purchase',
        'point_of_sale',
        'mrp',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'product.profile.csv',
    ],
    'demo': [
        'product_product_demo.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
