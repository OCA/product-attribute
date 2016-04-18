# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Pricelist Item Generator',
    'version': '8.0.0.0.1',
    'category': '',
    'summary': "Create/Update Pricelist Items in a massive way",
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale',
        ],
    'data': [
        'views/pricelist_view.xml',
        'views/setting_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/pricelist.item.generator.csv',
        'demo/pricelist.product.condition.csv',
        'demo/pricelist.item.template.csv',
    ],
    'installable': True,
    'images': [
    ],
}
