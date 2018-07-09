# -*- coding: utf-8 -*-
# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Use product supplier info for customers too",
    "version": "10.0.2.0.0",
    "author": "AvanzOSC, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Sales Management",
    "license": 'AGPL-3',
    "depends": [
        "base",
        "product",
        "purchase",
    ],
    "data": [
        "views/product_view.xml",
    ],
    "demo": [
        "demo/product_demo.xml",
    ],
    "installable": True,
}
