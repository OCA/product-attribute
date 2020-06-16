# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Application Custom Info',
    'version': '12.0.1.0.0',
    'development_status': "Mature",
    'category': 'Product',
    'summary': "Adds Custom Info to Product Applications",
    'author': 'PlanetaTIC'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'product_application',
        'base_custom_info',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_application_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
