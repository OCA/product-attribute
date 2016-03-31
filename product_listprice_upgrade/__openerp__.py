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
    "name":"Product listprice upgrade",
    "version":"1.0",
    "author":"Tiny",
    "category":"Generic Modules/Inventory Control",
    "description": """
    The aim of this module is to allow the automatic upgrade of the field 'List Price' on each product.
    * added a new price type called 'Internal Pricelist' (currently, we have only 2 price types: Sale and Purchase Pricelist)
    * Created a wizard button in the menu Products>Pricelist called 'Upgrade Product List Price'
    * When we have completed the wizard and click on 'Upgrade', it will change the field 'List Price' for all products contained in the categories that we have selected in the wizard
    """,
    "depends":["base","product"],
    "demo_xml":[],
    "update_xml":['product_wizard.xml','product_data.xml'],
    "active":False,
    "installable":False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

