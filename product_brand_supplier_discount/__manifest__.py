# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Brand Supplier Info',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'summary': "Assign a discount to the products of a brand when"
    " sold from an especific supplier",
    'author': 'PlanetaTIC'
              ' Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/brand',
    'license': 'AGPL-3',
    'depends': [
        'product_brand',
        'purchase_discount',
        'product_supplier_sale_price',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
