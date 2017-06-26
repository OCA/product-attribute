# coding: utf-8
# Copyright 2017 Vauxoo (https://www.vauxoo.com) info@vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Products Customer Code",
    "version": "8.0.1.0.0",
    "author": "Vauxoo, Odoo Community Association (OCA)",
    "category": "Generic Modules/Product",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
        "product"
    ],
    "demo": [],
    "data": [
        "security/product_customer_code_security.xml",
        "security/ir.model.access.csv",
        "views/product_customer_code_view.xml",
        "views/product_product_view.xml"
    ],
    "test": [],
    "installable": True,
    "auto_install": False,
}
