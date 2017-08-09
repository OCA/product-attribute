# -*- coding: utf-8 -*-
# Copyright 2009 NetAndCo (<http://www.netandco.net>).
# Copyright 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# Copyright 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# Copyright 2016 SerpentCS Pvt. Ltd. <http://www.serpentcs.com>
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Product Brand Manager',
    'version': '9.0.1.1.0',
    'category': 'Product',
    'summary': 'Product Brand Manager',
    'author': 'NetAndCo, '
              'Akretion, '
              'Prisnet Telecommunications SA, '
              'MONK Software, '
              'SerpentCS Pvt. Ltd., '
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': [
        'views/product_brand_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
