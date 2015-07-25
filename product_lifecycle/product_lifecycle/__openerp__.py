# -*- encoding: utf-8 -*-
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
###############################################################################
#    Credits:
#    Coded by: Katherine Zaoral <kathy@vauxoo.com>
#    Planified by: Nhomar Hernandez <nhomar@vauxoo.com>
#    Audited by: Nhomar Hernandez <nhomar@vauxoo.com>
###############################################################################
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
###############################################################################

{
    "name": "Product Lifecycle",
    "summary": "Manage replacement of discontinued products",
    "version": "1.5",
    "author": "Vauxoo",
    "website": "http://www.vauxoo.com/",
    "category": "product",
    "depends": [
        "product",
        "purchase",
        "purchase_order_line_sequence",
    ],
    "data": [
        "wizard/replacement_product_view.xml",
        "view/product_view.xml",
        "view/purchase_view.xml",
        "security/product_security.xml",
    ],
    "demo": [
        "demo/replacement_product_demo.xml",
    ],
    "test": [],
    "qweb": [],
    "js": [],
    "css": [],
    "installable": True,
}
