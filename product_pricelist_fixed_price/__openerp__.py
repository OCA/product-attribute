# -*- coding: utf-8 -*-
# © 2015 Therp BV (http://therp.nl).
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fixed price in pricelists",
    "version": "8.0.1.0.1",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza,"
              "Tecnativa,"
              "Therp BV,"
              "Odoo Community Association (OCA)",
    "category": "Sales Management",
    "website": "www.serviciosbaeza.com",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        'view/product_pricelist_item_view.xml',
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
}
