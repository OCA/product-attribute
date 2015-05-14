# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv, fields, expression
from openerp import SUPERUSER_ID


class product_product(osv.osv):
    _inherit = 'product.product'

    def _is_standard_price_visible_hook(self, cr, uid, ids, name, args,
                                        context=None):
        res = dict.fromkeys(ids, True)
        model_data_obj = self.pool.get('ir.model.data')
        res_groups_obj = self.pool.get('res.groups')
        for product in self.browse(cr, uid, ids, context=context):
            # Check if user belongs to the group
            group_id = model_data_obj._get_id(
                cr, uid, 'product_standard_price_visible',
                'group_product_standard_price_visible')
            if group_id:
                res_id = model_data_obj.read(cr, uid, [group_id],
                                             ['res_id'])[0]['res_id']
                group = res_groups_obj.browse(
                    cr, uid, res_id, context=context)
                group_user_ids = [user.id for user
                                  in group.users]
                group_user_ids.append(SUPERUSER_ID)
                if uid in group_user_ids:
                    res[product.id] = True
        return res

    def _is_standard_price_visible(self, cr, uid, ids, name, args,
                                   context=None):
        if context is None:
            context = {}
        return self._is_standard_price_visible_hook(
            cr, uid, ids, name, args, context=context)

    _columns = {
        'standard_price_visible': fields.function(
            _is_standard_price_visible,
            string="Standard price is visible",
            method=True, type='boolean')
    }