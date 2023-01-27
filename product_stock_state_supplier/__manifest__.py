# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Stock State Supplier",
    "summary": "Compute the state of a product's stock based on "
    "the state of the stock in the supplier",
    "version": "14.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product_stock_state"],
    "data": [
        "views/product_view.xml",
    ],
    "installable": True,
}
