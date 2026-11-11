# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Cost Security - HR Expense",
    "summary": "Glue module between product_cost_security and hr_expense",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product_cost_security", "hr_expense"],
    "data": ["views/hr_expense_views.xml"],
    "auto_install": True,
}
