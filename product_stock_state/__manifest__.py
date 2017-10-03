# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Product Stock State",
    "summary":
        "Compute the state stock based on"
        "the stock level and sale_ok field",
    "version": "10.0.1.0.0",
    "category": "Uncategorized",
    "website": "www.akretion.com",
    "author": " Akretion,GRAP",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_stock",
    ],
    "data": [
        'security/res_groups.xml',
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/product_category_view.xml',
        'views/sale_config_settings_view.xml',
    ],
    "demo": [
        'demo/res_groups.xml',
        'demo/product_category.xml',
        'demo/product_product.xml',
        'demo/product_category.xml',
    ],
    "qweb": [
    ]
}
