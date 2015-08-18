# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
    def _get_unit_price(self):
        for supplierinfo in self:
            unit_price = 0
            for item in supplierinfo.pricelist_ids:
                if item.min_quantity == 1:
                    unit_price = item.price
            supplierinfo.unit_price = unit_price

    unit_price = fields.Float(
        compute=_get_unit_price)
