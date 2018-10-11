# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
