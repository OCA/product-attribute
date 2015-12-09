# -*- coding: utf-8 -*-
# Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#                     All Rights Reserved.
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Pack',
    'summary': 'Sell groups of products as a product',
    'version': '8.0.2.0.0',
    'category': 'Product',
    'author':  'NaN·tic, '
               'ADHOC, '
               'Antiun Ingeniería S.L., '
               'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    "website": "http://www.antiun.com",
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pack_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
