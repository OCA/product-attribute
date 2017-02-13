# -*- coding: utf-8 -*-
# Copyright 2015 Akretion
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Pricelist Per Product",
    "summary": "Display pricelist items in products",
    "version": "9.0.1.0.0",
    "category": "Sales",
    "website": "http://www.akretion.com/",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "views/product_pricelist_view.xml",
        "views/product_pricelist_item_view.xml",
        "views/product_template_view.xml",
    ],
}
