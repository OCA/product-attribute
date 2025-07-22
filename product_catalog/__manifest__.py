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
            "product_catalog/static/src/product_catalog/search/search_panel.esm.js",
            "product_catalog/static/src/product_catalog/kanban_model.esm.js",
            "product_catalog/static/src/product_catalog/order_line/order_line.esm.js",
            "product_catalog/static/src/product_catalog/kanban_record.esm.js",
            "product_catalog/static/src/product_catalog/kanban_renderer.esm.js",
            "product_catalog/static/src/product_catalog/kanban_controller.esm.js",
            "product_catalog/static/src/product_catalog/kanban_view.esm.js",
        ],
    },
}
