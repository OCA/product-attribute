# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Category Tag",
    "version": "18.0.1.0.0",
    "summary": "Add tags to product categories",
    "website": "https://github.com/OCA/product-attribute",
    "author": "APSL-Nagarro, Odoo Community Association (OCA)",
    "maintainers": ["ppyczko"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "account", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_tag_views.xml",
        "views/product_category_views.xml",
    ],
}
