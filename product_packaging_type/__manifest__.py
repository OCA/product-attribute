# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Product Packaging Type',
    'version': '12.0.1.0.0',
    'development_status': "Beta",
    'category': 'Product',
    'summary': "Product Packagin Type",
    'author': 'Camptocamp, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'stock',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_packaging_type_view.xml',
        'views/product_packaging_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
