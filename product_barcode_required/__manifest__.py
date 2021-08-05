# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
{
    "name": "Product barcode required",
    "summary": "Make product barcode required when enabled",
    "version": "14.0.1.0.0",
    "maintainers": ["simahawk"],
    "development_status": "Beta",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["product"],
    "data": [
        "views/res_config_settings.xml",
        "views/product_template_view.xml",
        "views/product_view.xml",
    ],
}
