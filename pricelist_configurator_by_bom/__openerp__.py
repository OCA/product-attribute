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
different margins applied to the costs of the components of the bill of
material.
In OpenERP the product’s price is computed by the price list, every partner can
have his price list and every price list item con be connected to a product.

This module provides a configurator where the user selects the final product
and the partner. The system propose the BOM with the costs of every component.
The user can finally set the margin for every component and compute the final
price.

How To Use
----------
 - In the configurator, fill the Product and Partner fields, the system will
   automatically load the bom (changeable) and the lines
 - Work on the several lines setting the margin you want to apply
 - Compute the final price and create (or update) the price list
""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com/',
    'depends': ['product', 'sale', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'pricelist_configurator_by_bom_view.xml',
    ],
    'test': [
        'test/pricelist_configurator_by_bom.yml'
    ],
    'installable': True,
}
