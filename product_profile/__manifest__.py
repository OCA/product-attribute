# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Profile",
    "version": "10.0.1.0.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "summary": "Allow to configure a product in 1 click",
    "category": "product",
    "depends": ["sale"],
    "website": "http://www.akretion.com/",
    "data": [
        "security/group.xml",
        "views/product_view.xml",
        "views/config_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/product.profile.csv"],
    "installable": True,
    "license": "AGPL-3",
}
