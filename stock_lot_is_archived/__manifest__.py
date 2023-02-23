# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock Lot Is Archived",
    "summary": """
        This module adds a simple property on Lots that means a lot is archived""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_expiry", "stock"],
    "data": [
        "security/security.xml",
        "views/stock_lot.xml",
        "data/ir_cron.xml",
    ],
}
