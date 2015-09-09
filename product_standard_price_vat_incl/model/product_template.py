# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Standard Price VAT Included Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Column Section
    standard_price_vat_incl = fields.Float(
        compute='_compute_standard_price_vat_incl', string='Cost VAT Included',
        store=True, digits_compute=dp.get_precision('Product Price'),
        help="Cost price of the product:\n"
        "This cost will be 'Cost Price' x 'Customers Taxes'")

    @api.one
    @api.depends(
        'standard_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_standard_price_vat_incl(self):
        taxes = self.env['account.tax'].browse(self.taxes_id.ids)
        info = taxes.compute_all(self.standard_price, 1, force_excluded=True)
        self.standard_price_vat_incl = info['total_included']
