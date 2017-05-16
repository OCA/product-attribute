# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Product State",
    'description': """
        Module introducing a state field on product template""",
    'author': 'ACSONE SA/NV, Odoo Community Association (OCA)',
    'website': "http://acsone.eu",
    'category': 'Product',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'application': True,
}
