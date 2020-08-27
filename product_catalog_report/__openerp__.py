##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
    "name":"Product Catalog - Print Report of product catalog with product image",
    "version":"1.0",
    "author":"Tiny",
    "category":"Generic Modules/Inventory Control",
    "description": """
    This module use to print report of product catalog with product image, list price
    """,
    "depends":["base","product"],
    "demo_xml":[],
    "update_xml":['product_report.xml','product_wizard.xml'],
    "active":False,
    "installable":False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

