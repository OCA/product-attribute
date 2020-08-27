# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Production Lot Expiry",
    "summary": """
        This addon allows you to easily know if a lot is expired and search
        for expired lot.""",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["lmignon"],
    "website": "https://acsone.eu/",
    "depends": ["stock", "product_expiry"],
    "data": [
        "views/stock_production_lot.xml",
        "data/ir_config_parameter.xml",
        "views/product_category.xml",
        "views/product_template.xml",
        "wizards/stock_config_settings.xml",
    ],
    "demo": [],
    "pre_init_hook": "pre_init_hook",
}
