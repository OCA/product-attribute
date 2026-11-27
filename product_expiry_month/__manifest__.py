# Copyright (C) 2026 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Expiry Month",
    "summary": "Add expiration time in months field with automatic conversion to days",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_expiry"],
    "data": [
        "data/system_parameter_data.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
}
