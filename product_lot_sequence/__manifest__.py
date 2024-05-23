# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Lot Sequence",
    "summary": """
        Adds ability to define a lot sequence from the product""",
    "version": "16.0.1.0.2",
    "license": "AGPL-3",
    "author": "ForgeFlow S.L., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["stock"],
    "data": [
        "data/ir_config_parameter.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
