# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple images for products",
    "version": "1.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Antiun Ingeniería, "
              "Odoo Community Association (OCA)",
    "website": "http://www.serviciosbaeza.com",
    "category": "Sales Management",
    "depends": [
        "multi_image_base",
        "product",
    ],
    "data": [
        'views/product_product_view.xml',
    ],
    'installable': True,
}
