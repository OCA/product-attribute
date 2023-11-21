# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Product Packaging level purchasable",
    "summary": "Control purchase of products via packaging settings.",
    "version": "16.0.1.1.0",
    "development_status": "Alpha",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product_packaging_level", "purchase_stock"],
    "data": [
        "views/product_packaging_level.xml",
    ],
}
