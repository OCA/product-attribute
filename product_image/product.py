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
        return super(ProductProduct, self).\
            copy(cr, uid, id, default, context=context)

    def _get_main_image_id(self, cr, uid, product_id, context=None):
        product = self.read(cr, uid, product_id, ['image_ids'],
                            context=context)
        if product['image_ids']:
            return product['image_ids'][0]
        return None

    def __get_main_image(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        img_obj = self.pool.get('product.image')
        for product_id in ids:
            image_id = self._get_main_image_id(
                cr, uid, product_id, context=context)
            if image_id:
                image = img_obj.browse(cr, uid, image_id, context=context)
                res[product_id] = image[field_name]
            else:
                res[product_id] = None
        return res
    
    _columns = {
        'image_ids': fields.one2many(
                'product.image',
                'product_id',
                string='Product Image'),
        'image': fields.function(
            __get_main_image,
            type="binary",
            string="Main Image"),
        'image_medium': fields.function(
            __get_main_image,
            type="binary",
            string="Medium-sized image"),
        'image_small': fields.function(
            __get_main_image,
            type="binary",
            string="Small-sized image"),
        }
