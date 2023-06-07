# Copyright 2023 FactorLibre - Hugo Córdoba (hugo.cordoba@factorlibre.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Pricelist Simulation Margin",
    "summary": "Add margin of product price for all pricelists",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Odoo Community Association (OCA), FactorLibre",
    "maintainers": ["legalsylvain"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product_pricelist_simulation"],
    "data": [
        "wizards/wizard_preview_pricelist_views.xml",
    ],
}
