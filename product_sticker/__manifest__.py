# Copyright 2023 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Product Sticker",
    "version": "18.0.1.0.2",
    "author": "Moduon, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Sales Management",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_sticker_views.xml",
        "views/product_attribute_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "data/menus.xml",
    ],
    "maintainers": ["Shide", "rafaelbn"],
    "installable": True,
}
