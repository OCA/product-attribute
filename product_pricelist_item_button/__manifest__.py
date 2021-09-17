# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Item Button",
    "summary": """
        Allows to access to pricelist items tree view to get search features""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["rousseldenis"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product",
        "product_pricelist_button_box",
    ],
    "data": [
        "views/product_pricelist_item.xml",
        "views/product_pricelist.xml",
    ],
}
