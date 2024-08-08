# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Simple Seasonality",
    "summary": """
        Product seasonality""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "views/product_packaging.xml",
        "views/product_template.xml",
        "views/seasonality.xml",
        "security/seasonality.xml",
    ],
    "maintainers": ["bealdav", "kevinkhao"],
}
