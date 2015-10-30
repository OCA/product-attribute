# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Product category sequence",

    'summary': """
        Use a sequence to automatically fill the code""",

    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': "http://acsone.eu",

    'category': 'Generic Modules/Inventory Control',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',

    'depends': [
        'product_category_code',
    ],

    # always loaded
    'data': [
        'data/product_category_sequence.xml'
    ],
    'pre_init_hook': 'update_null_and_slash_codes',
    'installable': True,
}
