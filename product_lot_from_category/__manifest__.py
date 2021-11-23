# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Lot Category",
    "summary": """
        Allows to define lot tracking on category level""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "maintainers": ["rousseldenis"],
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "views/product_category.xml",
    ],
}
