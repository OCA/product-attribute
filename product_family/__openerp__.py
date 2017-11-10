# -*- coding: utf-8 -*-
# (c) 2017 Consultoría Informática Studio73 SL (contacto@studio73.es)
#          Pablo Fuentes <pablo@studio73.es>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Family',
    'summary': 'Product Family',
    'author': 'Consultoría Informática Studio 73 S.L.',
    'website': 'http://www.studio73.es',
    'category': 'Product',
    'version': '8.0.1.0.0',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/product_family_view.xml',
    ],
    'installable': True,
}
