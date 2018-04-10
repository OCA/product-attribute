# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Product Brand in Invoices Analysis',
    'version': '9.0.1.0.0',
    'category': 'Product',
    'author': 'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/account-invoice-reporting',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'product_brand',
    ],
    'data': [
        'reports/account_invoice_report_view.xml',
    ],
    'installable': True,
}
