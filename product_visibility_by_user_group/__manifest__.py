# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Visibility By User Group",
    "summary": "Restrict product visibility by user groups",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/product_template.xml",
        "security/product_product.xml",
        "views/product_template.xml",
    ],
    "maintainers": ["sbejaoui"],
}
