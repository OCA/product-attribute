# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product seasonality",
    "summary": "Define rules for products' seasonal availability",
    "version": "15.0.1.1.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Others",
    "depends": [
        # core
        "product",
        # oca/product-attribute
        "product_allowed_list",
    ],
    "website": "https://github.com/OCA/product-attribute",
    "data": [
        # Views
        "views/product_allowed_list_line.xml",
    ],
    "installable": True,
}
