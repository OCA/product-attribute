{
    "name": "Product Category Level",
    "summary": """
        Add Level field on Product Categories
        to show the recursion level on the category""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["PierrickBrun"],
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
