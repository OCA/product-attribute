# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Product Category Image',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Add image on product category',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    'depends': ['product'],
    'excludes': ['product_default_image'],
    'data': ['views/product_view.xml'],
    'installable': True,
}
