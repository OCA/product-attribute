# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Price List Tax Include",
    "summary": "Write product price list with taxes include",
    "version": "9.0.1.0.0",
    "category": "Product",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "views/product_view.xml",
    ],
    'post_init_hook': 'post_init_hook',
}
