# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Description Form',
    'summary': """
        Adds the description field in product form""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'maintainers': ['rousseldenis'],
    'depends': [
        'product',
    ],
    'data': [
        'views/product_template.xml',
    ],
}
