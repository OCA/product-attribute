# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015  KMEE  - www.kmee.com.br - Rodolfo Bertozo               #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from openerp.osv import orm, fields


class ProductProduct(orm.Model):
    _inherit = 'product.product'

    def create(self, cr, uid, vals, context=None):

        obj_categ = self.pool.get('product.category')
        categ = obj_categ.browse(cr, uid, vals['categ_id'])

        if categ.seq_id:
            prefix = ''
            ref = categ.default_code
            ref += self.pool.get('ir.sequence').next_by_id(
                cr, uid, categ.seq_id.id, context)

            while categ:
                sufix = prefix

                if categ.parent_id:
                    categ = obj_categ.browse(cr, uid, [categ.parent_id.id])[0]
                    prefix = (categ.default_code or '') + sufix
                else:
                    categ = False

            vals['default_code'] = prefix + ref

        return super(ProductProduct, self).create(cr, uid, vals, context)

    _columns = {
        'default_code': fields.char('Internal Reference', size=64, select=True),
    }


class ProductCategory(orm.Model):
    _inherit = "product.category"

    def create(self, cr, uid, vals, context=None):
        ref = ""
        poll_sequence = self.pool.get('ir.sequence')

        if vals['parent_id']:
            obj_parent = self.browse(cr, uid, vals['parent_id'])
            ref = poll_sequence.next_by_id(
                cr, uid, obj_parent.seq_id.id, context)

        elif not vals['seq_id']:
            ref = vals['default_code']

        else:
            ref = poll_sequence.next_by_id(cr, uid, vals['seq_id'], context)

        vals['default_code'] = ref

        return super(ProductCategory, self).create(cr, uid, vals, context)

    _columns = {
        'seq_id': fields.many2one('ir.sequence', 'Sequence'),
        'default_code': fields.char('Internal Reference', size=64),
    }
