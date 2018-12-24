# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Restricted Type',
    'version': '11.0.1.0.0',
    'author': "Eficent,"
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'category': 'Product',
    'depends': [
        'product',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'auto_install': False,
    'installable': True,
}
