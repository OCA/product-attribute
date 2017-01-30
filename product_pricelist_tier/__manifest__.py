# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Pricelist Tier",
    "summary": "Extends pricelists with tiered pricing.",
    "version": "10.0.1.0.0",
    "category": "Product",
    "website": "https://laslabs.com",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "post_init_hook": "_trigger_onchange_price_discount",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_pricelist_item_view.xml",
    ],
    "demo": [
        "demo/product_template_demo.xml",
        "demo/product_pricelist_item_demo.xml",
    ],
}
