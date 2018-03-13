# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product uom use type",
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
    ],
    "data": [
        'views/view_product_uom.xml',
    ],
    'demo': [
        'demo/product_uom_demo.xml'
    ]
}
