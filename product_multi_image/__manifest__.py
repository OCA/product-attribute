# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Products",
    "version": "10.0.1.0.0",
    "author": "Antiun Ingeniería, "
              "Tecnativa, "
              "LasLabs, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://www.tecnativa.com",
    "category": "Sales Management",
    "pre_init_hook": "pre_init_hook",
    "uninstall_hook": "uninstall_hook",
    "depends": [
        "base_multi_image",
        "product",
    ],
    "data": [
        'views/image_view.xml',
        'views/product_template_view.xml',
    ],
    'installable': True,
    "images": [
        "images/product.png",
        "images/db.png",
        "images/file.png",
        "images/url.png",
    ],
}
