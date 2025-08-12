# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Merge",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizards/product_merge_wizard.xml",
    ],
    "demo": [],
    "external_dependencies": {"python": ["openupgradelib"]},
}
