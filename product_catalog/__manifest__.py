# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Catalog",
    "summary": "Backport of Odoos v17 product catalog",
    "version": "16.0.1.0.0",
    "author": "Odoo SA, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        "web",
        "product",
        "sale",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/product_views.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "product_catalog/static/src/product_catalog/search/search_panel.xml",
            "product_catalog/static/src/product_catalog/search/search_panel.js",
            "product_catalog/static/src/product_catalog/kanban_model.js",
            "product_catalog/static/src/product_catalog/kanban_view.js",
        ],
    },
}
