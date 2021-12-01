# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Product Status",
    "summary": "Product Status Computed From Fields",
    "version": "14.0.1.0.0",
    "category": "Product",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product", "product_state"],
    "data": [
        "data/function_deactive_default_product_state_data.xml",
        "data/product_state_data.xml",
        "views/product_views.xml",
    ],
    "installable": True,
}
