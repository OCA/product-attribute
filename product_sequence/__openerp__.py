# -*- coding: utf-8 -*-
# © 2004 Tiny SPRL
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Sequence',
    'version': '9.0.1.0.0',
    'author': "Zikzakmedia SL,Sodexis,Odoo Community Association (OCA)",
    'website': 'http://www.zikzakmedia.com',
    'license': 'AGPL-3',
    'category': 'Generic Modules/Inventory Control',
    'depends': [
        'product',
    ],
    'data': [
        'data/product_sequence.xml',
    ],
    'demo': [
        'demo/product_product.xml'
    ],
    'pre_init_hook': 'update_null_and_slash_codes',
    'auto_install': False,
    'installable': True,
}
