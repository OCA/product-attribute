# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Lot Catalog",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["stock"],
    "data": [
        "views/stock_lot_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "lot_catalog/static/src/js/**/*",
            "lot_catalog/static/src/lot_catalog/**/*.js",
            "lot_catalog/static/src/lot_catalog/**/*.xml",
            "lot_catalog/static/src/lot_catalog/**/*.scss",
        ],
    },
    "maintainers": ["victoralmau"],
}
