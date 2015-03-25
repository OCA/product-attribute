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

class ProductPrice(orm.Model):
    '''Inherit existing model to add functionality for fixed prices'''
    _inherit = 'product.pricelist.item'

    def _price_field_get_ext(self, cr, uid, context=None):
        '''Added fixed price to pricetypes'''
        result = super(
            ProductPrice, self)._price_field_get(
                cr, uid, context=context)
        result.append((FIXED_PRICE_TYPE, _('Fixed Price')))
        return result

    _columns = {
        'base_ext': fields.selection(
            _price_field_get_ext, 'Based on',
            required=True, size=-1,
            help="Base price for computation."
        ),
    }
    _defaults = {
        'base_ext': -1,
    }

    def _check_fixed_price(self, cr, uid, ids):
        '''Ensure fixed prices always refer to a specific product.'''
        for this_obj in self.browse(cr, uid, ids):
            if not this_obj.base_ext == FIXED_PRICE_TYPE:
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
        (_check_fixed_price, 'invalid values for fixed price', ['base_ext']),
    ]

    def _auto_end(self, cr, context=None):
        '''Make sure that after updating database tables for this module,
        existing values in pricelist item are set correctly.'''
        cr.execute(
            'update product_pricelist_item'
            ' set base_ext = base'
            ' where base_ext != -3 and base != base_ext'
        )
        return super(ProductPrice, self)._auto_end(
            cr, context=context)

    def _modify_vals(self, cr, uid, vals, browse_obj=None, context=None):
        '''Ensure consistent values for fixed pricelist items.
        The passed vals parameter is used for both input and output.
        base should be 1 if base-ext = -1, in all other cases base and
        base_ext should be the same. The value passed should be leading,
        with the exception that a fixed price item should never be changed
        into something else through base.'''
        # Check wether any action is needed
        if not ('base_ext' in vals or 'base' in vals):
            return
        # Get base and base_ext values
        if 'base_ext' in vals:
            base_ext = vals['base_ext']
            if base_ext != FIXED_PRICE_TYPE:
                base = base_ext
            else:
                # Use id of first record in product.price.type (normally 1):
                base_id = self.pool['product.price.type'].search(
                    cr, uid, [], limit=1, order='id')
                assert base_id, _('No record found in product.price.type')
                base = base_id[0]
        else:
            # getting here we are sure base is in vals
            base = vals['base']
            # check against changing fixed price (should not happen)
            if browse_obj:
                assert browse_obj.base_ext != FIXED_PRICE_TYPE, (
                    _('Can not change fixed pricelist item through base'))
            base_ext = base
        # Synchronize base and base_ext values
        vals.update({
            'base_ext': base_ext,
            'base': base,
        })
        # Make sure other values valid for fixed price
        if base_ext == FIXED_PRICE_TYPE:
            vals.update({
                'price_discount': -1.0,
                'price_round': 0.0,
                'price_min_margin': 0.0,
                'price_max_margin': 0.0,
            })

    def create(self, cr, uid, vals, context=None):
        '''override create to get computed values'''
        self._modify_vals(cr, uid, vals, browse_obj=None, context=context)
        return super(ProductPrice, self).create(
            cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        '''override write to get computed values.
        We need the loop, because computed values might depend on existing
        values.'''
        if isinstance(ids, (int, long)):
            ids = [ids]
        for browse_obj in self.browse(cr, uid, ids, context=context):
            self._modify_vals(cr, uid, vals, browse_obj=browse_obj,
                              context=context)
            super(ProductPrice, self).write(cr, uid, browse_obj.id,
                                            vals, context=context)
        return True

    def onchange_base_ext(self, cr, uid, ids, base_ext, context=None):
        '''Make sure values for base and base_ext keep in sync in the UI'''
        vals = {'base_ext': base_ext}
        self._modify_vals(cr, uid, vals, context=context)
        return {'value': vals}
