# Copyright 2015 Anybox
# Copyright 2018 Camptocamp, ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product set",
    "category": "Sale",
    "license": "AGPL-3",
    "author": "Anybox, Odoo Community Association (OCA)",
    "version": "16.0.3.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "security/rule_product_set.xml",
        "views/product_set.xml",
        "views/product_set_line.xml",
    ],
    "demo": ["demo/product_set.xml", "demo/product_set_line.xml"],
    "installable": True,
}
