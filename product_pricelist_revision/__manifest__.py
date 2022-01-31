# Copyright 2018 Carlos Dauden - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Revision",
    "summary": "Product Pricelist Revision",
    "version": "14.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/pricelist_view.xml",
        "wizards/pricelist_duplicate_wizard_view.xml",
    ],
}
