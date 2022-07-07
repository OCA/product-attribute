# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product End-Of-Life Date",
    "summary": "Alert users when products approach EoL Date",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product", "stock", "purchase"],
    "data": [
        "views/product_view.xml",
        "views/purchase_view.xml",
        "views/res_config_settings_view.xml",
        "data/ir_cron.xml",
        "data/mail_channel_data.xml",
        "views/mail_templates.xml",
    ],
    "installable": True,
}
