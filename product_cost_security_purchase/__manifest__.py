# Copyright 2026 360ERP (<https://www.360erp.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Cost Security - Purchase",
    "summary": "Glue module between product_cost_security and purchase",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "360ERP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product_cost_security", "purchase"],
    "data": ["views/product_views.xml"],
    "auto_install": True,
}
