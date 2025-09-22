# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product battery",
    "summary": "Register batteries on products",
    "version": "16.0.1.0.0",
    "category": "product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template.xml",
    ],
}
