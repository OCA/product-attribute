# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Manufacturer',
    'version': '11.0.1.0.0',
    'summary': 'Adds manufacturers and attributes on the product view.',
    'author': 'OpenERP SA, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Product',
    'depends': ['product'],
    'data': [
        'views/product_manufacturer_view.xml',
    ],
    'auto_install': False,
    'installable': True,
}
