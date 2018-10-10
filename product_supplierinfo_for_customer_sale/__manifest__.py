# -*- coding: utf-8 -*-
# Copyright 2018 Vauxoo (https://www.vauxoo.com) info@vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Product supplier info for customer - sale",
    "version": "11.0.1.0.0",
    "author": "Vauxoo, Odoo Community Association (OCA)",
    "website": "http://www.vauxoo.com/",
    "category": "Sales Management",
    "license": 'AGPL-3',
    "depends": [
        "product_supplierinfo_for_customer",
        "sale",
    ],
    "data": [
        "views/sale_view.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": True,
}
