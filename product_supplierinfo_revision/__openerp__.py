# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Revision",
    "summary": "Customizations for Licores Reyes",
    "version": "9.0.1.0.0",
    "category": "Product",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa S.L.",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "views/product_supplierinfo_view.xml",
        "wizards/supplierinfo_duplicate_wizard_view.xml",
    ],
}
