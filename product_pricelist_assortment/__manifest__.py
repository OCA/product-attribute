# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Assortment",
    "summary": """
        Product assortment and pricelist""",
    "version": "13.0.1.0.1",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_assortment"],
    "data": [
        "security/product_pricelist_assortment_item.xml",
        "data/ir_cron.xml",
        "views/product_pricelist.xml",
        "views/product_pricelist_assortment_item.xml",
        "views/product_pricelist_item.xml",
    ],
    "demo": [],
}
