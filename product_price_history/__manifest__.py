# Copyright 2020 Andrea Piovesana (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Product Price History View",
    'summary': "Product Price History View",
    'description': "Product Price History View",
    'version': '11.0.1.0.0',
    'category': 'Product',
    'author': 'Pordenone Linux User Group (PNLUG), Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': [
        'product',
    ],
    'data': [
        'views/product_price_history_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
