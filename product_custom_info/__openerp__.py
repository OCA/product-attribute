# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': "Product Custom Info",
    'summary': "Add custom field in products",
    'category': 'Customize',
    'version': '8.0.1.0.0',
    'depends': [
        'product',
        'base_custom_info',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Incaser Informatica S.L., ',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
