# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, api
from openerp.models import Model
from openerp.tools.translate import _


class ProductSupplierinfo(Model):
    _inherit = 'product.supplierinfo'

    @api.multi
    def _get_unit_price(self):
        for supplierinfo in self:
            if len(supplierinfo.pricelist_ids) == 0:
                supplierinfo.unit_price = 0
                supplierinfo.unit_price_note = _('-')
            elif len(supplierinfo.pricelist_ids) == 1:
                item = supplierinfo.pricelist_ids[0]
                supplierinfo.unit_price = item.price
                if item.min_quantity not in (0, 1):
                    supplierinfo.unit_price_note = _("%s (Min Qty: %s)" % (
                        item.price, item.min_quantity))
                else:
                    supplierinfo.unit_price_note = item.price
            else:
                min_qty = max_qty = supplierinfo.pricelist_ids[0].min_quantity
                min_price = max_price = supplierinfo.pricelist_ids[0].price
                for item in supplierinfo.pricelist_ids:
                    if item.min_quantity < min_qty:
                        min_qty = item.min_quantity
                        min_price = item.price
                    if item.min_quantity > max_qty:
                        max_qty = item.min_quantity
                        max_price = item.price
                supplierinfo.unit_price = min_price
                supplierinfo.unit_price_note = _(
                    "%s (Min Qty: %s) >> %s (Min Qty: %s)" % (
                        min_price, min_qty, max_price, max_qty))

    unit_price_note = fields.Char(
        compute=_get_unit_price, multi='unit_price', string='Unit Price')

    unit_price = fields.Float(
        compute=_get_unit_price, multi='unit_price',
        help="""Purchase Price of the product for this supplier. \n If many"""
        """ prices are defined, The price will be the price associated with"""
        """ the smallest quantity.""")
