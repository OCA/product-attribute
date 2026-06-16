# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Attribute Groupby Filter",
    "summary": "Allow grouping by attributes in product tree view.",
    "version": "14.0.0.1.0",
    "category": "product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["Kev-Roche"],
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "views/assets.xml",
        "views/product_attribute.xml",
        "views/product_product.xml",
        "views/res_config_settings.xml",
    ],
    "qweb": [
        "static/src/xml/product_attribute_groupby.xml",
    ],
}
