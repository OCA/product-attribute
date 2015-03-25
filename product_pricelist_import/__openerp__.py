
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 08/10/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Product Pricelist Import",
    "version": "1.0",
    "description": """
    This module allows to load product price list from a file.
    The file format must have these colummns:

    keys = ['code', 'info', 'price', 'discount_1', 'discount_2', 'retail',
    'pdv1', 'pdv2']
    """,
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    'website': "http://www.odoomrp.com",
    "depends": ['purchase'],
    "category": "Manufacturing",
    "data": ['wizard/import_price_file_view.xml',
             'views/product_pricelist_load_line_view.xml',
             'views/product_pricelist_load_view.xml',
             'security/ir.model.access.csv'
             ],
    "installable": True
}
