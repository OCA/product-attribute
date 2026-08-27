# Copyright (C) 2025 - Today: Gemini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Substate",
    "summary": "Adds substate support to products.",
    "version": "19.0.1.0.0",
    "category": "Product",
    "author": "OBS Solutions,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product_state", "base_substate"],
    "data": [
        "views/product_template_views.xml",
    ],
    "demo": [
        "demo/product_substate_demo.xml",
    ],
    "installable": True,
}
