# -*- coding: utf-8 -*-
##############################################################################
#
# Author: Leonardo Donelli @ Creativi Quadrati
# Copyright (C) 2014 Leonardo Donelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Product Unique Code',
    'version': '1.0',
    'category': 'Product',
    'description': """
Product Unique Codes
===========================
Enforce a unique constraint on the internal (default) product code.
It also makes it required, because it doesn't make sense to have an unique
field that can be null.
""",
    'author': 'Creativi Quadrati',
    'website': 'http://www.creativiquadrati.it',
    'depends': ['product'],
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
