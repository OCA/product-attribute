# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Template Tags',
    'summary': """
        This addon allow to add tags on products""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV, Omal Bastin, Odoo Community Association (OCA)',
    'website': 'https://www.acsone.eu',
    'depends': [
        'product',
    ],
    'data': [
        'security/product_template_rule.xml',
        'security/product_template_tag.xml',
        'views/product_template.xml',
        'views/product_template_tag.xml',
    ],
    'installable': True,
}
