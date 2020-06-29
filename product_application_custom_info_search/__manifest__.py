# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Application Custom Info Search',
    'version': '12.0.1.0.0',
    'development_status': "Mature",
    'category': 'Product',
    'summary': "Search products by product applications",
    'author': 'PlanetaTIC'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'product_application_custom_info',
    ],
    'data': [
        'views/sale_view.xml',
        'wizard/filter_application_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
