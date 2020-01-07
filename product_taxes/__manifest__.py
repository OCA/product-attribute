# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Taxes',
    'version': '11.0.1.0.0',
    'category': 'Product',
    'author': 'Camptocamp SA, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'product',
    ],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'images': [
        'static/description/icon.png',
    ],
}
