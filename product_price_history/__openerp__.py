# Copyright 2020 Andrea Piovesana (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Product Cost Price History Views",
    'summary': "Handle standard price history records",
    'version': '8.0.1.0.0',
    'category': 'Product',
    'author': 'Pordenone Linux User Group (PNLUG),'
              'Odoo Community Association (OCA)',
    'maintainers': ["marcelofrare", "andreampiovesana"],
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/product_price_history_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
