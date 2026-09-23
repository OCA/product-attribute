# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging Template",
    "summary": """Allows to define product packaging at template level""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
    ],
    "data": [
        "security/groups.xml",
        "security/product_packaging_template.xml",
        "views/product_template.xml",
        "views/product_packaging_template.xml",
    ],
    "installable": True,
}
