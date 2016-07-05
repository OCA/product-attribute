# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'product_custom_attributes',
    'version': '9.0.1.0',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """This module adds the possibility to easily create custom fields on products.
Each product can be linked to an attribute set (like camera, fridge...).
Each attribute has custom fields (for example, you don't need the same field for a frigde and a camera).
In particular it's used by the Magento Magentoerpconnect module to match the EAV flexibility of Magento.
    """,
    'author': "Akretion,Odoo Community Association (OCA)",
    'website': 'http://www.akretion.com/',
    'depends': ['product', 'base_custom_attributes'],
    'init_xml': [],
    'update_xml': [
           'views/product_view.xml',
           'views/custom_attributes_view.xml',
           'wizard/open_product_by_attribute_set.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}

