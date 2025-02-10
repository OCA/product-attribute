# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Expiry Alert",
    "summary": """This module allows to compute expiry alerts on product lots""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["rousseldenis"],
    "depends": [
        "product_expiry",
    ],
    "data": [
        "views/stock_lot.xml",
        "views/stock_quant.xml",
    ],
}
