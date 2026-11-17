# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging Template Sales",
    "summary": """Adds the 'Sales' information on packaging template level""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
        "sale",
        "product_packaging_template",
    ],
    "data": [
        "views/product_packaging_template.xml",
    ],
    "installable": True,
}
