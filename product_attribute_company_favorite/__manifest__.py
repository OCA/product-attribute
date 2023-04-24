# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Product Attribute Company Favorite",
    "summary": """
        Possibility to set favorite product attributes per company""",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "product",
        "stock",
    ],
    "excludes": [],
    "data": [
        "views/product_attribute_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_init_hook": "initialize_attribute_is_favorite_field",
}
