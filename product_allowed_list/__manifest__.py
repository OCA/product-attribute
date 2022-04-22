# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Allowed Lists",
    "summary": "Define rules for products' allowed list",
    "version": "15.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Others",
    "depends": [
        # core
        "product",
    ],
    "website": "https://github.com/OCA/product-attribute",
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Views
        "views/product_list.xml",
        "views/product_list_line.xml",
        "views/res_company.xml",
        "views/res_partner.xml",
    ],
    "installable": True,
}
