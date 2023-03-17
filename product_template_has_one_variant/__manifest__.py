# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Template Has One Variant",
    "summary": """
        Allows to define a field on product template level to determine
        if it has only one variant""",
    "version": "16.0.1.0.1",
    "license": "AGPL-3",
    "maintainers": ["rousseldenis"],
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "views/product_template.xml",
    ],
}
