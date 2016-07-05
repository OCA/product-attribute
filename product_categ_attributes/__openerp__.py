# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'product_categ_attributes',
    'version': '9.0.1.0',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """Makes it possible to inherit product attributes from its categories
    """,
    'author': "Akretion,Odoo Community Association (OCA)",
    'website': 'http://www.akretion.com/',
    'depends': ['product_custom_attributes', 'product_multi_category'],
    'init_xml': [],
    'update_xml': [
        "views/product_view.xml"
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}

