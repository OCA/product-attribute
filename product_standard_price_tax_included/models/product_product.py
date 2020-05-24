# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Column Section
    standard_price_tax_included = fields.Float(
        compute='_compute_standard_price_tax_included',
        string='Cost Price Tax Included',
        digits=dp.get_precision('Product Price'),
        help="Cost Price of the product, All Tax Included:\n"
        "This field will be computed with the 'Cost Price', taking into"
        " account Sale Taxes setting.")

    @api.depends('standard_price', 'taxes_id')
    def _compute_standard_price_tax_included(self):
        for product in self:
            info = product.taxes_id.with_context(
                force_price_include=False,
                use_force_price_include=True).compute_all(
                    product.standard_price, quantity=1, product=product)
            product.standard_price_tax_included = info['total_included']
