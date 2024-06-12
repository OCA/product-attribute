# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Internal Reference as Required",
    "summary": "Set Product Internal Reference as a required field",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
    ],
    "data": [
        "data/product_code_seq.xml",
        "views/product_view.xml",
    ],
    "pre_init_hook": 'pre_init_product_code',
    "installable": True,
}
