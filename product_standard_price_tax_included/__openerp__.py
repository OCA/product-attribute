# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product - Cost Price Tax Included',
    'version': '8.0.2.1.0',
    'category': 'Product',
    'summary': 'Brings a Cost Price Field Tax Included on Product Model',
    'author': 'GRAP,Odoo Community Association (OCA)',
    'website': 'http://www.odoo-community.org',
    'license': 'AGPL-3',
    'development_status': 'Beta',
    'maintainers': ['legalsylvain'],
    'depends': [
        'product',
        'sale',
        'account',
    ],
    'data': [
        'data/product_price_type.xml',
        'views/view_product_template.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_pricelist.xml',
        'demo/res_partner.xml',
        'demo/account_tax.xml',
        'demo/product_template.xml',
    ],
}
