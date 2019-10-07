# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Documentation Sets",
    "summary": """
        Manage Product Documentation""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/product_documentation_set.xml",
        "views/product_documentation_set.xml",
        "views/product_template.xml",
        "views/product_category.xml",
    ],
}
