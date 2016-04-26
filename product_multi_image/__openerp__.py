# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Products",
    "version": "8.0.2.0.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Antiun Ingeniería, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.serviciosbaeza.com",
    "category": "Sales Management",
    "pre_init_hook": "pre_init_hook",
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
