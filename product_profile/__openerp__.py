# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Profile',
    'version': '8.0.1.0.0',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'summary': "Set a configuration profile to product templates",
    'category': 'product',
    'depends': [
        'product',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'security/group.xml',
        'product_view.xml',
        'config_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/product.profile.csv',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
