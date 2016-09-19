# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Product Bundle',
    'summary': 'Sell groups of products as a product',
    'version': '9.0.1.0.0',
    'category': 'Product',
    'author': 'Tecnativa,'
              'Odoo Community Association (OCA)',
    "license": "LGPL-3",
    "website": "https://www.tecnativa.com",
    'depends': [
        'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_bundle_line_view.xml',
        'views/product_view.xml',
        'views/procurement_order_view.xml',
        'views/stock_move_view.xml',
    ],
    'demo': [
        'demo/products.yml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
