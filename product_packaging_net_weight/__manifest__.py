# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging Net Weight",
    "summary": "Add the net weight on product packagings",
    "version": "19.0.1.0.0",
    "category": "Product",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product_packaging", "product_net_weight"],
    "data": [
        "views/product_packaging_views.xml",
    ],
    "auto_install": True,
    "installable": True,
}
