# Copyright 2025 Juan Carlos Oñate - Tecnativa <juancarlos.onate@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product EPREL",
    "summary": "Manage EPREL model identifiers and energy label data for products.",
    "version": "14.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
        "data/eprel_cron.xml",
        "data/eprel_product_categories.xml",
    ],
    "demo": [
        "demo/product_template.xml",
    ],
    "installable": True,
}
