# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of product_brand_sequence,
#     an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     product_brand_sequence is free software:
#     you can redistribute it and/or modify it under the terms of the GNU
#     Affero General Public License as published by the Free Software
#     Foundation,either version 3 of the License, or (at your option) any
#     later version.
#
#     product_brand_sequence is distributed
#     in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#     even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with product_brand_sequence.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Product brand sequence",

    'summary': """
        Use a sequence to automatically fill the reference""",

    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': "http://acsone.eu",

    'category': 'Generic Modules/Inventory Control',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',

    'depends': [
        'product_brand',
    ],

    'data': [
        'data/product_brand_sequence.xml'
    ],
    'pre_init_hook': 'update_null_and_slash_codes',
    'installable': True,
}
