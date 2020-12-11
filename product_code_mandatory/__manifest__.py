# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Code Mandatory",
    "summary": "Set Product Internal Reference as a required field",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": ["data/product_code_seq.xml", "views/product_view.xml"],
    "pre_init_hook": "pre_init_product_code",
    "installable": True,
}
