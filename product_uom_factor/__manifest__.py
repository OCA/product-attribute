# Copyright 2026 Bemade Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product UoM Conversion Factor",
    "summary": "Product-specific conversion factors for cross-category UoM conversions",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "author": "Bemade Inc., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["mdurepos"],
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
}
