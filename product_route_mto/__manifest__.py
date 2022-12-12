# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Route Mto",
    "summary": """
        This module allows to compute if a product is an 'MTO' one from its
        configured routes""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "stock_route_mto",
    ],
    "data": [
        "views/product_template.xml",
    ],
}
