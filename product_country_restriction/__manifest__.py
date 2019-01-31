# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Country Restriction',
    'summary': """
        Allows to define product restrictions country based""",
    'version': '10.0.1.1.1',
    'development_status': 'Alpha',
    'maintainers': ['rousseldenis'],
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'security/product_country_restriction.xml',
        'views/product_country_restriction.xml',
        'views/product_country_restriction_item.xml',
        'views/product_country_restriction_rule.xml',
        'views/res_country.xml',
        'views/res_partner.xml',
        'data/product_country_restriction_rule.xml',
    ],
    'demo': [
        'demo/product_country_restriction.xml',
    ],
}
