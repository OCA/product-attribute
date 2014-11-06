# -*- coding: utf-8 -*-
{
    'name': 'base_custom_attributes',
    'version': '0.1.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """
This module adds the possibility to easily create custom attributes in any
 OpenERP business object. See the product_custom_attributes
 module for instance.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['base'],
    "license": "AGPL-3",
    'data': ['security/ir.model.access.csv',
             'security/attribute_security.xml',
             'custom_attributes_view.xml'],
    'installable': True,
    'external_dependencies': {'python': ['unidecode']}

}
