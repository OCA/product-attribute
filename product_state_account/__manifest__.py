# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State Account",
    "summary": "Restrict invoicing of products based on their product state",
    "author": "glueckkanja AG, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["product_state", "account"],
    "data": [
        "views/product_state_views.xml",
        "views/account_move_views.xml",
    ],
    "auto_install": True,
}
