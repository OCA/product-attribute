# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Author: Nicola Malcontenti <nicola.malcontenti@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': 'Pricelist Configurator By Bom',
    'version': '0.1',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'description': """
Introduction
------------
This module is a calculator that establishes the final product’s price based on
various margins on the single cost of the bill of material. In OpenERP the
product’s price is on the price list, every partner can have his price list and
every price list is connected to a product. So this is a calculator for the
price list.

This module provides a configurator where the user selects the final product
and the partner. The system propose the BOM with the cost of every component.
The User can finally set the margin for every component.

How To Use
----------
 - In the configurator, fill the Product and Partner fields, the system will
   automatically set the bom (changeable) and the lines
 - Work on the several lines
 - Create or Update the Price List
 - Compute the final price

    """,
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com/',
    'depends': ['product', 'sale', 'mrp'],
    'init_xml': [],
    'data': [
            'pricelist_configurator_by_bom_view.xml',
    ],
    'update_xml': [
        'security/ir.model.access.csv'
    ],
    'test': [
        'test/pricelist_configurator_by_bom.yml'
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
