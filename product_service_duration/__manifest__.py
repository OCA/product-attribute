# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Service Duration",
    "summary": "Extends events and meetings with services.",
    "version": "10.0.1.0.0",
    "category": "Product",
    "website": "https://laslabs.com",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "calendar",
        "resource",
    ],
    "data": [
        "views/calendar_event_view.xml",
        "views/product_product_view.xml",
    ],
    "demo": [
        "demo/product_product_demo.xml",
        "demo/calendar_event_demo.xml",
    ],
}
