# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com> 
#                  2014 Therp BV (http://www.therp.nl)
#
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
#
##############################################################################
'''All functionality to enable fixed prices in pricelists.'''
from openerp.osv import orm, fields
from openerp.tools.translate import _


FIXED_PRICE_TYPE = -3

class product_pricelist_item(orm.Model):
    '''Inherit existing model to add functionality for fixed prices'''
    _inherit = 'product.pricelist.item'

    def _price_field_get_ext(self, cr, uid, context=None):
        result = super(
            product_pricelist_item, self)._price_field_get(
                cr, uid, context=context)
        result.append((FIXED_PRICE_TYPE, _('Fixed Price')))
        return result

    _columns = {
        'base_ext': fields.selection(_price_field_get_ext, 'Based on',
                                     required=True, size=-1,
                                     help="Base price for computation."),
    }
    _defaults = {
        'base_ext': -1,
    }

    def _check_fixed_price(self, cr, uid, ids):
        '''Ensure fixed prices always refer to a specific product.'''
        for this_obj in self.browse(cr, uid, ids):
            if this_obj.base_ext == FIXED_PRICE_TYPE:
                return True
            if not this_obj.product_id:
                raise orm.except_orm(
                    _('Validation error!'),
                    _('Product required for fixed price item.')
                )
            # Values for price_discount and price_round will not be checked,
            # because create and write will automagically set appropiate
            # values.
        return True

    _constraints = [
        (_check_fixed_price,
            'invalid values for fixed price', ['base_ext']),
    ]

    def _modify_vals(self, cr, uid, vals, browse_obj=None, context=None):
        '''Ensure consistent values for fixed pricelists.
        The passed vals parameter is used for both input and output.'''
        # First determine wether a fixed price should apply
        fixed_price = False
        if browse_obj:
            fixed_price = (browse_obj.base_ext == FIXED_PRICE_TYPE)
        else:
            # new record
            fixed_price = (
                'base_ext' in vals and
                vals['base_ext'] == FIXED_PRICE_TYPE or False)
        if not fixed_price:
            return
        vals.update({
            'price_discount': -1.0,
            'price_round': 0.0,
            'base': 1,
            'price_min_margin': 0.0,
            'price_max_margin': 0.0,
        })

    def create(self, cr, uid, vals, context=None):
        '''override create to get computed values'''
        self._modify_vals(cr, uid, vals, browse_obj=None, context=context)
        return super(product_pricelist_item, self).create(
            cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        '''override write to get computed values.
        We need the loop, because computed values might depend on existing
        values.'''
        for object_id in ids:
            browse_records = self.browse(
                cr, uid, [object_id], context=context)
            browse_obj = browse_records[0]
            self._modify_vals(
                cr, uid, vals, browse_obj=browse_obj, context=context)
            super(product_pricelist_item, self).write(
                cr, uid, [object_id], vals, context=context)
        return True

    def onchange_base_ext(self, cr, uid, ids, base_ext, context=None):
        vals = {'base_ext': base_ext}
        self._modify_vals(cr, uid, vals, context=context)
        return {'value': vals}

