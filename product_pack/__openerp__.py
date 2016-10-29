# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (c) 2009 Angel Alvarez - NaN  (http://www.nan-tic.com)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    @author Albert Cervera i Areny <albert@nan-tic.com>
#    @author Franco Tampieri <franco.tampieri@agilebg.com>
#    Ported to OpenERP 7.0 by Alex Comba <alex.comba@agilebg.com>
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
###############################################################################
{
    "name": "Product Pack",
    "version": "0.2",
    "category": "Warehouse Management",
    "description": """
Based on the NAN_product_pack this module allows configuring products
as a collection of other products.
If such a product is added in a sale order or a purchase order, all the
products of the pack will be added automatically (when storing the order)
as children of the pack product.
    """,
    "author": "Agile Business Group & NaN·tic",
    "website": "http://www.agilebg.com",
    "depends": [
        'sale',
        'purchase',
    ],
    "data": [
        'security/ir.model.access.csv',
        'pack_view.xml'
    ],
    "active": False,
    "installable": True
}
