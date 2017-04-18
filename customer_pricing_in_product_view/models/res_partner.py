# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution - module extension
#    Copyright (C) 2014- O4SB (<http://o4sb.com>).
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

from ast import literal_eval

from openerp.osv import orm


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def view_partner_pricing(self, cr, uid, ids, context=None):
        """
        This function is primarily triggered by the 'Products Pricing'
        smart button on the partner form.  It returns the default product
        list action with context adjusted to set the default pricelist to
        the id of the partner
        :param cr: database cursor
        :param uid: user id
        :param ids: partner ids (list of one)
        :param context:
        :return:
        """
        mod_obj = self.pool['ir.model.data']
        result = mod_obj.get_object_reference(
            cr, uid, 'product', 'product_normal_action_sell')
        id = result and result[1] or False
        result = self.pool['ir.actions.act_window'].read(cr, uid, [id],
                                                         context=context)[0]
        partner = self.pool['res.partner'].browse(cr, uid, ids,
                                                  context=context)[0]
        act_ctx = literal_eval(result['context'])
        act_ctx.update({'search_default_pricelist_id':
                        partner.property_product_pricelist.id})
        result['context'] = unicode(act_ctx)
        return result
