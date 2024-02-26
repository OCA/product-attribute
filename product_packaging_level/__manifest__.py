# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Product Packaging Level",
    "version": "16.0.1.2.0",
    "development_status": "Beta",
    "category": "Product",
    "summary": "This module binds a product packaging to a packaging level",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "LGPL-3",
    "depends": ["product", "stock"],
    "data": [
        "data/product_packaging_level.xml",
        "security/ir.model.access.csv",
        "views/product_packaging_level_view.xml",
        "views/product_packaging_view.xml",
        "views/stock_package_type_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "external_dependencies": {"python": ["openupgradelib"]},
    "pre_init_hook": "pre_init_hook",
}
