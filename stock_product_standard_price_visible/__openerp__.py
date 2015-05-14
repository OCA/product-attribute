# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
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
    'name': 'Product stock standard price visible',
    'version': '1.0',
    'author': 'Eficent',
    "website": "www.eficent.com",
    'category': 'Products',
    'depends': ['product_cost_security', 'stock'],
    'demo': [],
    'description': """
Product stock standard price visible
====================================
This module restricts the visibility of the field 'cost' associated to the
product only to users that belong to the group 'Display product cost',
in stock-related views.


Installation
============

No specific installation steps are required.

Configuration
=============

No specific configuration steps are required.

Usage
=====

No specific usage instructions are required.


Known issues / Roadmap
======================

No issues have been identified with this module.

Credits
=======

Contributors
------------

* Moises Lopez <moylop260@vauxoo.com>
* Jordi Ballester Alomar <jordi.ballester@eficent.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
    """,
    'data': [
        'view/product.xml',
        'report/report_stock_move_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'images': [],
}
