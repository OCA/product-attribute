# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Pricelist Alternative",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Calculate product price based on alternative pricelists",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_pricelist_item_view.xml",
        "views/product_pricelist_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
