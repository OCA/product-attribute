# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Category Code Unique",
    "summary": """
        Allows to set product category code field as unique""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["rousseldenis"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
        "product_category_code",
    ],
    "post_init_hook": "post_init_hook",
}
