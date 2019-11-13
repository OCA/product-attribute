# Copyright 2017 LasLabs Inc.
# Copyright 2020 initOS GmbH.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Default Product Images",
    "summary": "Apply default images to new and existing products.",
    "version": "11.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "initOS GmbH, LasLabs, Odoo Community Association (OCA)",
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
        "views/res_config_settings_view.xml",
        "views/product_template_view.xml",
    ],
    "demo": [
        "demo/res_company_demo.xml",
        "demo/product_category_demo.xml",
        "demo/product_template_demo.xml",
    ],
}
