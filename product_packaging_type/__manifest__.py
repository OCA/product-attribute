# -*- coding: utf-8 -*-
# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Product Packaging Type",
    "version": "10.0.1.2.1",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Product Packaging Type",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "LGPL-3",
    "depends": ["product", "product_packaging_barcode", "stock"],
    "data": [
        "data/product_packaging_type.xml",
        "security/ir.model.access.csv",
        "views/assets_backend.xml",
        "views/product_packaging_type_view.xml",
        "views/product_packaging_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
