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
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """

    """,
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com/',
    'depends': ['product','sale','mrp'],
    'init_xml': [],
    'data': [
           'pricelist_configurator_by_bom_view.xml',
           'test/pricelist_configurator_by_bom.yml'
    ],
    'test': [
        'test/pricelist_configurator_by_bom.yml'
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}