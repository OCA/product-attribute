# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   base_attribute.attributes for OpenERP                                     #
#   Copyright (C) 2015 Odoo Community Association (OCA)                       #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

{
    'name': 'Product Custom Attributes',
    'version': '1.0',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'author': "Akretion,"
    "Odoo Community Association (OCA),"
    "Savoir-faire Linux",
    'website': 'https://github.com/OCA/product-attribute/',
    'depends': [
        'product',
        'base_custom_attributes',
        'sale',
    ],
    'data': [
        'views/attribute_set.xml',
        'views/attribute_group.xml',
        'views/attribute_attribute.xml',
        'views/product.xml',
        'views/product_category.xml',
        'wizard/open_product_by_attribute_set.xml',
        'wizard/product_product.xml',
    ],
    'demo_xml': [],
    'installable': True,
}
