# Copyright 2014-2018 Therp BV <https://therp.nl>.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Show product relations in own tab",
    "version": "12.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "category": "Product",
    "depends": [
        'product_multi_relation',
    ],
    "demo": [
        "demo/product_category_demo.xml",
        "demo/product_demo.xml",
        "demo/product_tab_demo.xml",
        "demo/product_relation_type_demo.xml",
        "demo/product_relation_demo.xml",
    ],
    "data": [
        "views/product_tab.xml",
        "views/product_relation_type.xml",
        "views/product_relation_all.xml",
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
