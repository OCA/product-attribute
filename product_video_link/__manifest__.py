# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Video",
    "summary": "Link Video on product and category",
    "version": "14.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product",
        "base_video_link",
    ],
    "data": [
        "views/product_category_view.xml",
        "views/product_template_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/product_demo.xml"],
}
