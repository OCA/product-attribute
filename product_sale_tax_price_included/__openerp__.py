# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product sale tax price included",
    "summary": "Module summary",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/product-attribute",
    "author": "GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product",
        "account",
    ],
    "data": [
        'views/product_template.xml',
    ],
    "demo": [
        'demo/account_tax_demo.xml',
        'demo/product_template_demo.xml'
    ],
}
