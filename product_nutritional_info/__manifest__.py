# Copyright 2020 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Product Nutritional Info",
    'summary': """
        Module introducing a nutritional info field on product template""",
    'author': 'Xtendoo, Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/product-attribute",
    'category': 'Product',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'application': True,
}
