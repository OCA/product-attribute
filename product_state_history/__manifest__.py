# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State History",
    "summary": """
        Require a reason when changing product state and keep a dedicated history""",
    "version": "19.0.1.0.0",
    "category": "Product",
    "author": "AGF Vector GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product_state"],
    "data": [
        "security/product_state_history_security.xml",
        "security/ir.model.access.csv",
        "views/product_state_history_views.xml",
        "views/product_template_views.xml",
        "wizards/product_state_change_views.xml",
    ],
    "installable": True,
    "application": False,
    "maintainers": ["flogruber"],
}
