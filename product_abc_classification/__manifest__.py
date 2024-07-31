# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Abc Classification",
    "summary": """
        ABC classification for sales and warehouse management""",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product", "stock"],
    "data": [
        "views/abc_classification_product_level.xml",
        "views/abc_classification_profile.xml",
        "views/product_template.xml",
        "views/product_product.xml",
        "views/product_category.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
    ],
}
