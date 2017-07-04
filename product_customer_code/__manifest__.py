# -*- coding: utf-8 -*-
# Copyright 2012 Vauxoo - http://www.vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Products Customer Code",
    'version': '10.0.1.0.0',
    "author": "Vauxoo,Odoo Community Association (OCA)",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "category": "Generic Modules/Product",
    "summary": "Add many Customers' Codes in product",
    "depends": [
        "account",
        "product",
    ],
    "data": [
        "security/product_customer_code_security.xml",
        "security/ir.model.access.csv",
        "views/product_customer_code_view.xml",
        "views/product_product_view.xml",
        "views/res_partner_view.xml",
    ],
    'installable': True,
}
