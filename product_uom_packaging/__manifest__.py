# Copyright 2025 Bemade Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product UoM Packaging",
    "summary": """
        Link products to UoMs with package type for dimensions""",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "author": "Bemade Inc., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["mdurepos"],
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_uom_packaging_views.xml",
        "views/product_product_views.xml",
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
    ],
    "assets": {
        "web.assets_unit_tests": [
            "product_uom_packaging/static/tests/**/*",
            ("remove", "product_uom_packaging/static/tests/tours/**/*"),
        ],
        "web.assets_tests": [
            "product_uom_packaging/static/tests/tours/**/*",
        ],
    },
}
