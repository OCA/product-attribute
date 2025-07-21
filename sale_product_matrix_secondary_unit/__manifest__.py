# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Secondary unit in product matrix",
    "version": "17.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Sales Management",
    "maintainers": ["carlos-lopez-tecnativa"],
    "depends": [
        "sale_management",
        "sale_product_matrix",
        "sale_order_secondary_unit",
    ],
    "data": [
        "views/sale_order_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_product_matrix_secondary_unit/static/src/js/sale_product_field.esm.js",
            "sale_product_matrix_secondary_unit/static/src/js/product_matrix_dialog.esm.js",
            "sale_product_matrix_secondary_unit/static/src/xml/**/*",
        ],
        "web.assets_tests": [
            "sale_product_matrix_secondary_unit/static/tests/tours/**/*",
        ],
    },
}
