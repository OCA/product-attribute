# coding: utf-8
##############################################################################
#
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
    'name': 'Supplier on product_product',
    'summary': 'Allow to set supplier on product',
    'description': 'Because setting supplier on template is not enough',
    'version': '0.3',
    'author': 'Akretion',
    'maintainer': 'Akretion',
    'category': 'product',
    'depends': [
        'product',
        'purchase',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'views/product_view.xml',
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'tests': [],
    'installable': True,
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': [],
    },
}
