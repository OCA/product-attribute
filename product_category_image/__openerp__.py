# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


{'name': 'product_category_image',
 'version': '0.0.1',
 'author': 'Akretion',
 'website': 'www.akretion.com',
 'license': 'AGPL-3',
 'category': 'Generic Modules',
 'description': """
This module add the posibility to add an image to a
category. This can be usefull for e-commerce purpose,
for product paper catalog, for quotation that need image
related to the category of the product ...

Note : for now this module only add the support of one image,
some e-commerce give the posbility to manage various images
but in practice customer rarely use it because it's too much aditionnal work.

Depending of the need of the next customer we may implement the support
of multi-image, but as we want a really simple UI we stick on one image
 """,
 'depends': [
     'product',
     'binary_field',
 ],
 'data': [
     'product_view.xml',
 ],
 'installable': True,
 'application': True,
}




