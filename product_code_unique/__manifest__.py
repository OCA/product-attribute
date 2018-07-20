# -*- coding: utf-8 -*-
# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Unique Product Internal Reference',
    'summary': 'Set Product Internal Reference as Unique',
    'version': '10.0.1.0.0',
    'category': 'Product',
    'website': 'https://github.com/OCA/product-attribute',
    'author': 'Open Source Integrators, Akretion, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'pre_init_hook': 'pre_init_product_code',
    'depends': ['product'],
}
