# Copyright 2026 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Product Price History",
    "summary": "Track product price history within pricelists",
    "version": "18.0.1.1.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "APSL-Nagarro, Odoo Community Association (OCA)",
    "maintainers": ["peluko00"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pricelist_item_history_views.xml",
    ],
}
