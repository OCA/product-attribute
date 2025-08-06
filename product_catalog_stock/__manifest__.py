# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Product Catalog",
    "summary": "Use the product catalog on stock pickings",
    "version": "18.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["stock"],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_picking_type_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_catalog_stock/static/src/**/*",
        ],
    },
}
