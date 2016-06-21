# -*- coding: utf-8 -*-
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Pricelist rules list view",
    "summary": "View and search the list of pricelist items",
    "version": "9.0.1.0.0",
    "category": "Sales Management",
    "website": "https://www.agilebg.com",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        'views/pricelist_view.xml',
    ],
}
