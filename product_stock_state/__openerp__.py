# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Stock State",
    "summary":
        "Compute the state stock based on"
        "the stock level and sale_ok field",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "www.akretion.com",
    "author": " Akretion",
    "license": "AGPL-3",
    "application": False,
    'installable': False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_stock",
    ],
    "data": [
        'views/product_view.xml',
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
