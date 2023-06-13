# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Category Code Unique",
    "summary": """
        Allows to set product category code field as unique""",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["rousseldenis", "luisg123v"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
        "product_category_code",
    ],
    "data": [
        "data/product_category_sequence.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
