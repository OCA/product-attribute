# -*- coding: utf-8 -*-
##############################################################################
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "Product Variant Default Code",
    "version": "10.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "contributors": [
        "OdooMRP team",
        "Avanzosc",
        "Serv. Tecnol. Avanzados - Pedro M. Baeza",
        "Shine IT(http://www.openerp.cn)",
        "Tony Gu <tony@openerp.cn>",
        "Graeme Gellatly <g@o4sb.com>",
        ],
    "license": "AGPL-3",
    "category": "Product",
    "website": "http://www.odoo-community.org",
    "depends": ['product',
                'product_attribute_priority'
                ],
    "data": ['views/product_attribute_value_view.xml',
             'views/product_view.xml',
             ],
    "installable": True
}
