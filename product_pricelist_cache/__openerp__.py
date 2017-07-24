# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Cache product prices per pricelist',
    'version': '8.0.1.0.0',
    'author': 'Therp BV, Odoo Community Association (OCA)',
    'summary': 'Cache product prices',
    'category': 'Sales Management',
    'depends': [
        'product',
    ],
    'website': 'https://therp.nl/',
    'data': [
        'security/ir.model.access.csv',
        'data/product_price_cache_cron.xml',
        'views/product_price_cache.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
