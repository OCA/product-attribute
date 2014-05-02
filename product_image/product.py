# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions
#   Copyright (C) 2011-TODAY Akretion (http://www.akretion.com).
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


class ProductProduct(orm.Model):
    _inherit = "product.product"

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'image_ids': False,
        })
        return super(product_product, self).copy(cr, uid, id, default, context=context)

    def get_main_image(self, cr, uid, id, context=None):
        if isinstance(id, list):
            id = id[0]
        images_ids = self.read(cr, uid, id, ['image_ids'], context=context)['image_ids']
        if images_ids:
            return images_ids[0]
        return False

    def _get_main_image(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        img_obj = self.pool.get('product.images')
        for id in ids:
            image_id = self.get_main_image(cr, uid, id, context=context)
            if image_id:
                image = img_obj.browse(cr, uid, image_id, context=context)
                res[id] = image.file
            else:
                res[id] = False
        return res

    _columns = {
        'image_ids': fields.one2many(
                'product.image',
                'product_id',
                string='Product Image'),
        'product_image': fields.function(
            _get_main_image,
            type="binary",
            string="Main Image"),
    }
