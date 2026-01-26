# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Pricelist Filter",
    "summary": "Add domain on pricelist Item",
    "version": "18.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": " Akretion, Odoo Community Association (OCA)",
    "maintainers": ["mathieudelva"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product",
        "sale_management",
    ],
    "data": ["views/product_pricelist.xml"],
}
