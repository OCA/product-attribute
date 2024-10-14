# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Product Catalog",
    "summary": "Backport of Odoos v17 product catalog for sale orders",
    "version": "16.0.1.0.0",
    "author": "Odoo SA, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["sale", "product_catalog"],
    "data": [
        "views/sale_order_views.xml",
    ],
}
