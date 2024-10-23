# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Expiry Configurable",
    "summary": """
        This model allows setting expiry times on category and
         to use the 'end_of_life' date for the computation of lot dates""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_expiry"],
    "data": [
        "data/product_expiry_data.xml",
        "views/product_category.xml",
        "views/stock_lot.xml",
    ],
}
