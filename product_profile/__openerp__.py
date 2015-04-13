# -*- coding: utf-8 -*-
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
    'name': 'Product Profile',
    'version': '0.2',
    'author': 'Akretion',
    'summarize': "Set a configuration profile to product templates",
    'maintainer': 'Akretion',
    'description': "Profile",
    'depends': [
        'sale',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'product_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/product.profile.csv',
    ],
    'tests': [],
    'installable': True,
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': [],
    },
}
