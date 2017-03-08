# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Direct Print",
    "summary": "Print price list from menu option, product templates, "
               "products variants or price lists",
    "version": "9.0.1.0.0",
    "category": "Product",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/report_product_pricelist.xml",
        "wizards/product_pricelist_print_view.xml",
    ],
}
