# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Assortment',
    'summary': """
        Adds the ability to manage products assortment""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://acsone.eu',
    'depends': [
        'base',
        'product',
        'web_widget_domain_v11',
    ],
    'data': [
        'views/product_assortment.xml',
    ],
}
