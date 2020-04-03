# Copyright 2013-2017 Therp BV <http://therp.nl>
# Copyright 2020 Radovan Skolnik, KEMA SK
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Relations",
    "version": "12.0.1.0.0",
    "author": "Therp BV,Camptocamp,Odoo Community Association (OCA), Radovan Skolnik, KEMA SK",
    "website": "https://github.com/OCA/partner-contact",
    "complexity": "normal",
    "category": "Product",
    "license": "AGPL-3",
    "depends": [
        'product',
    ],
    "demo": [
        "data/demo.xml",
    ],
    "data": [
        'security/ir.model.access.csv',
        "views/product_relation_all.xml",
        'views/product.xml',
        'views/product_relation_type.xml',
        'views/menu.xml',
    ],
    "auto_install": False,
    "installable": True,
}
