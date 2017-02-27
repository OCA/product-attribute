# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: el_rodo_1 (rodo@vauxoo.com)
############################################################################

{
    "name": "Products Customer Code",
    'version': '10.0.1.0.0',
    "author": "Vauxoo,Odoo Community Association (OCA)",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "category": "Generic Modules/Product",
    "summary": "Add many Customers' Codes in product",
    "depends": [
        "base",
        "product",
    ],
    "description": """
Customer' codes in product
==========================

This module does just like the product.supplierinfo but for customers instead.
For instance it allows to have different references for the same product
according to the customer.

.. image:: product_customer_code/static/src/img/screenshot1.png

.. tip::

    You will need install some of the Apps which enable the product menu to
    see this module in action, like Sales, Purchase or Warehouse Management
     """,
    "data": [
        "security/product_customer_code_security.xml",
        "security/ir.model.access.csv",
        "views/product_customer_code_view.xml",
        "views/product_product_view.xml",
        "views/res_partner_view.xml",
    ],
    'installable': True,
}
