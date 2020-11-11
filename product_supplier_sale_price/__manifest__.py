# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Supplier Sale Price',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'summary': "Set Sale Price using prices suggested by supplier",
    'author': 'PlanetaTIC',
    'website': 'https://www.planetatic.com',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale',
        'product_variant_sale_price',
    ],
    'data': [
        'views/res_config_settings_view.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
