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


class ProductSupplierinfo(Model):
    _inherit = 'product.supplierinfo'

    @api.multi
    def _compute_unit_price(self):
        for supplierinfo in self:
            if len(supplierinfo.pricelist_ids) == 0:
                supplierinfo.unit_price = 0
                supplierinfo.unit_price_note = '-'
            else:
                txt = ''
                size = len(supplierinfo.pricelist_ids)
                uom_precision = supplierinfo.product_tmpl_id.uom_id.rounding
                for i in range(size - 1):
                    txt += '%s - %s :  %s\n' % (
                        supplierinfo.pricelist_ids[i].min_quantity,
                        (supplierinfo.pricelist_ids[i + 1].min_quantity -
                         uom_precision),
                        supplierinfo.pricelist_ids[i].price)
                txt += '>=%s : %s' % (
                    supplierinfo.pricelist_ids[size - 1].min_quantity,
                    supplierinfo.pricelist_ids[size - 1].price)
                supplierinfo.unit_price = supplierinfo.pricelist_ids[0].price
                supplierinfo.unit_price_note = txt

    unit_price_note = fields.Char(
        compute='_compute_unit_price', multi='unit_price', string='Unit Price')

    unit_price = fields.Float(
        compute='_compute_unit_price', multi='unit_price',
        help="""Purchase Price of the product for this supplier. \n If many"""
        """ prices are defined, The price will be the price associated with"""
        """ the smallest quantity.""")
