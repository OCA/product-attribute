# -*- coding: utf-8 -*-
# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Abc Classification",
    "summary": """
        ABC classification for sales and warehouse management""",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, ForgeFlow, Odoo Community Association (OCA)",
    "depends": ["product", "stock", "web_m2x_options"],
    "data": [
        "views/abc_classification_product_level.xml",
        "views/abc_classification_profile.xml",
        "views/product_template.xml",
        "views/product_product.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
    ],
    "demo": [],
}
