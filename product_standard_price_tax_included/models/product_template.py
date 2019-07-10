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
        string='Cost Price Tax Included', company_dependent=True,
        digits=dp.get_precision('Product Price'),
        help="Cost Price of the product, All Tax Included:\n"
        "This field will be computed with the 'Cost Price', taking into"
        " account Sale Taxes setting.")

    @api.multi
    @api.depends(
        'standard_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_standard_price_tax_included(self):
        for template in self:
            info = template.taxes_id.compute_all(
                template.standard_price, 1, force_excluded=True)
            template.standard_price_tax_included = info['total_included']
