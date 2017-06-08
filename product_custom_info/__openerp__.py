# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Sergio Teruel
# © 2015 Antiun Ingeniería S.L. - Carlos Dauden
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

{
    'name': "Product Custom Info",
    'summary': "Add custom field in products",
    'category': 'Customize',
    'version': '9.0.1.0.0',
    'depends': [
        'product',
        'base_custom_info',
    ],
    'data': [
        'views/product_product_view.xml',
        'views/product_template_view.xml',
    ],
    'author': "Tecnativa, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.tecnativa.com',
    'license': 'LGPL-3',
    'installable': True,
}
