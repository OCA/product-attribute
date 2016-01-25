# coding: utf-8
# © 2015 Sylvain CALADOR @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Pricelist Per Product',
    'version': '8.0.1.0.0',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'summarize': 'Display pricelist items in products',
    'maintainer': 'Akretion',
    'category': 'sale',
    'depends': [
        'sale',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'install_view.xml',
        'product_view.xml',
        'pricelist_view.xml',
        'data/pricelist.xml',
    ],
    'demo': [
        'demo/product.pricelist.item.csv',
    ],
    'tests': [],
    'images': [
        'static/description/mass.png',
        'static/description/pricelist.png',
        'static/description/product.png',
    ],
    'installable': True,
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': [],
    },
}
