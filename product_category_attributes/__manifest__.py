# Copyright 2020 Versada UAB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Category Attributes",
    "summary": "Restrict attributes/values per product category",
    "version": "14.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Versada UAB, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category.xml",
        "views/product_template.xml",
    ],
}
