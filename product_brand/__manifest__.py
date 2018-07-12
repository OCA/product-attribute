# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Product Brand Manager',
    'version': '11.0.1.1.0',
    'category': 'Product',
    'summary': "Product Brand Manager",
    'author': 'NetAndCo, Akretion, Prisnet Telecommunications SA, '
              'MONK Software, SerpentCS Pvt. Ltd., Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        ],
    'data': [
        'views/product_brand_view.xml',
        'reports/sale_report_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
