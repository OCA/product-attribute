# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Products Customer Code',
    'version': '8.0.1.0.0',
    'summary': 'Add many Customers Codes in product',
    'author': 'Vauxoo,Odoo Community Association (OCA)',
    'website': 'http://www.vauxoo.com/',
    'category': 'Generic Modules/Product',
    'depends': ['base', 'product'],
    'data': [
        'security/product_customer_code_security.xml',
        'security/ir.model.access.csv',
        'views/product_customer_code_view.xml',
        'views/product_product_view.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
