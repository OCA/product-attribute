# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product State History",
    "summary": """
        Allows to store product state history for reporting purpose""",
    "version": "14.0.1.0.2",
    "license": "AGPL-3",
    "category": "Sales",
    "maintainers": ["rousseldenis"],
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product_state",
    ],
    "data": [
        "security/product_state_history.xml",
        "security/product_state_history_wizard.xml",
        "views/product_state_history.xml",
        "views/product_template.xml",
        "wizards/product_state_history_wizard.xml",
        "report/report_product_state_history.xml",
    ],
}
