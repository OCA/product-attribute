# Copyright 2023 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy<raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Catalog",
    "summary": "Manage set of products",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "maintainers": ["hparfr"],
    "depends": [
        "product_assortment",
        "sale_management",  # for the menu
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_catalog.xml",
        "views/product_product.xml",
    ],
    "demo": [],
}
