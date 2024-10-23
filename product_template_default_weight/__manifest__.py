# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Template Default Weight",
    "version": "16.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "summary": "",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["mathieudelva"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["stock", "delivery"],
    "data": [
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
