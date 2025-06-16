# Copyright 2025 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Multi Attribute Value",
    "summary": "additional prices for multi attribute value on a pricelist item",
    "version": "16.0.1.0.0",
    "category": "sale",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["Kev-Roche"],
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "views/product_pricelist_item.xml",
        "security/ir.model.access.csv",
    ],
}
