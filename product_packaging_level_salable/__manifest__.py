# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Product Packaging level salable",
    "summary": "",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product_packaging_level", "sale_stock"],
    "data": [
        "views/product_packaging_level.xml",
    ],
}
