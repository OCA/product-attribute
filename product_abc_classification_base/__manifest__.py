# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Alc Product Abc Classification",
    "summary": """
        ABC classification for sales and warehouse management""",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "depends": ["product"],
    "data": [
        "views/product_category.xml",
        "views/product_template.xml",
        "views/abc_classification_profile.xml",
    ],
    "demo": [],
}
