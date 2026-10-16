# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging",
    "summary": "Product packagings with variant barcodes on product forms",
    "version": "19.0.1.0.0",
    "category": "Product",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_packaging_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
