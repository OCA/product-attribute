# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Default Product Images",
    "summary": "Apply default images to new and existing products.",
    "version": "10.0.1.0.0",
    "category": "Product",
    "website": "https://laslabs.com",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "post_init_hook": "find_templates_with_imgs",
    "depends": [
        "stock",
    ],
    "images": [
        'static/src/img/glob_prod_img.png',
    ],
    "data": [
        "views/product_category_view.xml",
        "views/stock_config_settings_view.xml",
        "views/product_template_view.xml",
    ],
    "demo": [
        "demo/res_company_demo.xml",
        "demo/product_category_demo.xml",
        "demo/product_template_demo.xml",
    ],
}
