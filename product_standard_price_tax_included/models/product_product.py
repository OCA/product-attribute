# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_price_tax_included = fields.Float(
        compute="_compute_standard_price_tax_included",
        string="Cost Price Tax Included",
        digits="Product Price",
        help="Cost Price of the product, All Tax Included:\n"
        "This field will be computed with the 'Cost Price', taking into"
        " account Sale Taxes setting.",
    )

    @api.depends_context("company")
    @api.depends("standard_price", "taxes_id", "taxes_id.price_include")
    def _compute_standard_price_tax_included(self):
        # Depends on force_company context because standard_price is company_dependent
        for product in self:
            info = product.taxes_id.compute_all(
                product.standard_price,
                quantity=1,
                product=product,
                handle_price_include=False,
            )
            product.standard_price_tax_included = info["total_included"]
