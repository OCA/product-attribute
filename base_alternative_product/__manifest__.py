# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Alternative Product",
    "summary": "Base Alternative Product",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/base_alternative_products_security.xml",
        "views/product_views.xml",
        "views/res_config_settings.xml",
        "wizards/alternative_product_wizard_views.xml",
    ],
}
