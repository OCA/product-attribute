# -*- coding: utf-8 -*-
{
    'name': 'product_custom_attributes',
    'version': '0.2.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """This module adds the possibility to easily create
 custom fields on products.\nEach product can be linked to an attribute set
 (like camera, fridge...).\n Each attribute has custom fields (for example,
 you don't need the same field for a frigde and a camera).\nIn particular it's
 used by the Magento Magentoerpconnect module to match the EAV flexibility of
 Magento.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    "license": "AGPL-3",
    'depends': ['product', 'base_custom_attributes'],
    'data': ['product_view.xml',
             'custom_attributes_view.xml',
             'wizard/open_product_by_attribute_set.xml'],
    'installable': True
}
