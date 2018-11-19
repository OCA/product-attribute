# Copyright 2018 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Weight Through UoM',
    'summary': 'Calculate product weight based on UoM',
    'version': '11.0.1.0.0',
    'category': 'Product',
    'author': 'Tecnativa,'
    'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': ['views/product_views.xml'],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
