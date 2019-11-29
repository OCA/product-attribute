# Copyright 2017 LasLabs Inc.
# © initOS GmbH 2019
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Product Service Duration",
    "summary": "Extends events and meetings with services.",
    "version": "11.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "initOS GmbH, LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale",
        "calendar",
        "resource",
    ],
    "data": [
        "demo/resource_demo.xml",
        "views/calendar_event_view.xml",
        "views/product_product_view.xml",
    ],
    "demo": [
        "demo/product_product_demo.xml",
        "demo/calendar_event_demo.xml",
    ],
}
