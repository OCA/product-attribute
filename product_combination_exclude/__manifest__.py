# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Combination Exclude',
    'summary': "Allows the specification of incompatible product "
               "combinations when creating products",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Graeme Gellatly,Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org',
    'depends': ['product', 'sale'],
    'data': [
        'security/product_attribute_exclude.xml',
        'security/product_attribute_exclude_matrix.xml',
        'views/product_attribute_exclude_matrix.xml',
    ],
    'demo': [
        'demo/product_attribute_exclude_matrix.xml',
        'demo/create_variants.xml'
    ],
}
