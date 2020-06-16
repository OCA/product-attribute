# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Application',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'summary': "List of product applications on product.template",
    'author': 'PlanetaTIC'
              ' Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_application_view.xml',
        'views/product_template_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
