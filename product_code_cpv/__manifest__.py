# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Common Procurement Vocabulary (CPV) codes',
    'version': '10.0.1.0.0',
    'author': "http://bitwise.solutions, Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'category': 'Purchase Management',
    'description': 'CPV Codes for Products',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'data/product_template_cpv.xml',
        'views/product_template.xml',
        'views/product_template_cpv.xml',
    ],
    'application': False,
    'installable': True,
}
