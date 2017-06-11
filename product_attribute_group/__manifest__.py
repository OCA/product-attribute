# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Attribute Group',
    'summary': """
        Allows grouping of product attributes for easy addition
        to a product template""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA)',
    'website': 'http://odoo-community.org',
    'depends': [
        'product', 'sale', 'sales_team'
    ],
    'data': [
        'security/product_attribute_group.xml',
        'views/product_attribute_group.xml',
        'views/product_template.xml',
    ],
    'demo': ['demo/product_demo.xml']
}
