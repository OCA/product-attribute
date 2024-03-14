# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Packaging Container Deposit",
    "version": "16.0.1.1.1",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Add container deposit fees in a order",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "product_packaging_level",
    ],
    "data": [
        "views/stock_package_type_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
