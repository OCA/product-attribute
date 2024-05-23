# Copyright 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Optional Product Quantity",
    "version": "16.0.1.1.0",
    "category": "Product",
    "summary": "Specify optional products quantity for product",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "sale_product_configurator",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
