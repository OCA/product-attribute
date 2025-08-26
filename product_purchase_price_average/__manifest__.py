# Copyright 2025 360ERP (<https://www.360erp.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Product Purchase Price Average",
    "summary": """Average purchase prices for products""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "360 ERP,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["purchase"],
    "data": [
        "views/product_template.xml",
        "data/cron.xml",
    ],
    "demo": [],
}
