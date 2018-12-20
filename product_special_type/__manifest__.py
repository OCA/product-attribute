# -*- coding: utf-8 -*-
# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Special Types',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Product',
    'development_status': 'Beta',
    'maintainers': ['rousseldenis'],
    'summary':
    '''
        Add a special type selection on products.
    ''',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': [
        'product'
    ],
    'data': [
        'views/product_template.xml',
    ],
    'installable': True,
}
