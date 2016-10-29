# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoirfaire-Linux Inc. (<www.savoirfairelinux.com>).
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

{
    'name': 'Product Dependencies',
    'version': '1.0',
    'category': 'Product Management',
    'description': """
Allows products to have other products/categories as dependencies.

This module is primarily used by the contract_isp_wizard module to create packages based on basic product selections but it can be used by others modules that manage product lists.""",
    'author': 'Savoirfaire-Linux Inc',
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': ['product_dependencies_view.xml'],
    'active': False,
    'installable': True,
}
