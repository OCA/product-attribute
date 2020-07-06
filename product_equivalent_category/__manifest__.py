# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Equivalent Category',
    'summary': """
        This module adds the concept of equivalent category. A product can
        belong to a certain equivalent category and all products in that
        category will be considered equivalent.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ForgeFlow S.L., Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': [
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_equivalent_category_views.xml',
        'views/product_template_views.xml',
    ],
    'demo': [
    ],
}
