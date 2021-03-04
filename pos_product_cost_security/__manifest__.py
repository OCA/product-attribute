# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "PoS Product Cost Security",
    "summary": "Compatibility between Point of Sale and Product Cost Security",
    "version": "14.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["product_cost_security", "point_of_sale"],
    "data": [
        "views/assets.xml",
    ],
}
