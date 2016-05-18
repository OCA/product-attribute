# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Products Customer Code",
    "version": "1.0",
    "author": "Vauxoo,Odoo Community Association (OCA)",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "category": "Generic Modules/Product",
    "summary": "Add many Customers' Codes in product",
    "depends": ["base", "product"],
    "data": [
        'security/product_customer_code_security.xml',
        'security/ir.model.access.csv',
        'views/product_customer_code_view.xml',
        'views/product_product_view.xml',
    ],
    'installable': True,
}
