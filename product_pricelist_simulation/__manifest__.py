# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Pricelist Simulation",
    "summary": "Simulate the product price for all pricelists",
    "version": "13.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product"],
    "data": [
        "wizard/pricelist_simulation.xml",
        "views/product_view.xml",
        "views/pricelist_view.xml",
    ],
}
