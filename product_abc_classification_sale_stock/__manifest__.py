# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Abc Classification based on delivered products",
    "summary": """
        Compute ABC classification from the number of delivered sale order
        line by product""",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "depends": ["product_abc_classification_base", "sale_stock"],
    "data": [
        "views/abc_classification_product_level.xml",
        "security/abc_sale_stock_level_history.xml",
        "views/abc_sale_stock_level_history.xml",
        "views/abc_classification_profile.xml",
    ],
    "demo": [
        "demo/abc_classification_level.xml",
        "demo/abc_classification_profile.xml",
    ],
}
