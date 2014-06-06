# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions
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

from openerp.osv import fields, orm
import os


class ProductImage(orm.Model):
    "Products Image"
    _name = "product.image"
    _order='sequence,name'

    _columns = {
        'sequence': fields.integer('Sequence'),
        'name': fields.char('Image Title'),
        'file_name': fields.char('File name', required=True),
        'description': fields.text('Description'),
        'image': fields.ImageField('Image'),
        'image_medium': fields.ImageResizeField(
            related_field='image',
            string='Image',
            height=128,
            width=128,
            ),
        'image_small': fields.ImageResizeField(
            related_field='image',
            string='Image',
            height=64,
            width=64,
            ),
        'product_id': fields.many2one('product.product', 'Product'),
    }

    _defaults= {
        'sequence': 0,
    }

    def onchange_name(self, cr, uid, ids, file_name, name, context=None):
        if not name:
            name, extension = os.path.splitext(file_name)
            for mapping in [('_', ' '), ('.', ' ')]:
                name = name.replace(mapping[0], mapping[1])
            return {'value': {'name': name}}
        return {}
