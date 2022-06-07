# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Template Tags Group',
    'summary': "This addon allow to group tags on products",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'TAKOBI, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': [
        'product_template_tags',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/product_template_tag_group_rule.xml',
        'views/product_template_tag_group_views.xml',
        'views/product_template_tag_views.xml',
    ],
}
