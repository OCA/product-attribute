# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#    Copyright (C) 2015 Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{'name': 'Product Weight Calculation',
 'version': '8.0.0.2.0',
 'author': 'Savoir-faire Linux,Akretion,Odoo Community Association (OCA)',
 'website': 'http://www.savoirfairelinux.com',
 'license': 'AGPL-3',
 'category': 'Warehouse',
 'summary': 'Allows to calculate products weight from its components.',
 'depends': ['mrp',
             ],
 'data': ['wizard/product_weight_update_view.xml',
          'product_view.xml',
          ],
 'installable': True,
 }
