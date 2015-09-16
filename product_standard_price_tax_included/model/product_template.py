# -*- coding: utf-8 -*-
##############################################################################
#
#    Product - Cost Price Tax Included Module for Odoo
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
    standard_price_tax_included = fields.Float(
        compute='_compute_standard_price_tax_included',
        string='Cost Price Tax Included',
        store=True, digits=dp.get_precision('Product Price'),
        help="Cost Price of the product, All Tax Included:\n"
        "This field will be computed with the 'Cost Price', taking into"
        " account Sale Taxes setting.")

    @api.one
    @api.depends(
        'standard_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_standard_price_tax_included(self):
        taxes = self.env['account.tax'].browse(self.taxes_id.ids)
        info = taxes.compute_all(self.standard_price, 1, force_excluded=True)
        self.standard_price_tax_included = info['total_included']
