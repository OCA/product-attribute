# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).
# © 2009 Sharoon Thomas Open Labs Business Solutions
# © 2014 Serv. Tecnol. Avanzados Pedro M. Baeza
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# © 2016 Pedro M. Baeza, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Products",
    "version": "9.0.1.0.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Antiun Ingeniería, Tecnativa, Sodexis, "
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
