# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Vincent Renaville. Copyright 2014 Camptocamp SA
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
    "name": "Product supplier check",
    "version": "1.0",
    "author": "Camptocamp",
    "website": "http://www.camptocamp.com/",
    "license": "AGPL-3",
    "category": "Generic Modules/Product",
    "summary": "Add check supplier on product",
    "depends": [
            "base",
            "product",
    ],
    "description": """
Supplier product check
==========================
Add constraint that check that the supplier set
for the product is not the company
     """,
    "data": [
    ],
    "active": False,
    "installable": True,
}
