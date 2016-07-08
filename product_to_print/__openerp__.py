# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product - To Print',
    'summary': 'Automate products print, when data has changed',
    'version': '9.0.1.0.0',
    'category': 'Product',
    'author': 'La Louve, Odoo Community Association (OCA)',
    'website': 'http://www.lalouve.net/',
    'depends': [
        'product',
        'stock',
        'web_kanban_gauge',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_category_print.xml',
    ],
    'data': [

        'security/ir.model.access.csv',
        'views/action.xml',
        'views/view_product_product.xml',
        'views/view_product_category_print.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
