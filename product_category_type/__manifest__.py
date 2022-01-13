# Copyright 2021 Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Category Type",
    "summary": """
        Add Type field on Product Categories
        to distinguish between parent and final categories""",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_category.xml",
    ],
    "demo": [
        "demo/product_category.xml",
    ],
}
