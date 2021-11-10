# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Revision",
    "version": "14.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_supplierinfo_view.xml",
        "wizards/supplierinfo_duplicate_wizard_view.xml",
    ],
}
