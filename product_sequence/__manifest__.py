# -*- coding: utf-8 -*-
# Copyright 2004 Tiny SPRL
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Sequence",
    "version": "10.0.2.0.0",
    "author": "Zikzakmedia SL,Sodexis,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "depends": ["product_code_unique"],
    "data": ["data/product_sequence.xml"],
    "pre_init_hook": "pre_init_hook",
    "auto_install": False,
    "installable": True,
}
