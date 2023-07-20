# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Product Top Category",
    "summary": """Compute the Top Category of Products""",
    "version": "12.0.1.0.1",
    "category": "Sale",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "product",
    ],
    "excludes": [],
    "data": ["views/product_category.xml"],
    "demo": [],
    "qweb": [],
}
