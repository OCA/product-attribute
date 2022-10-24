# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_price_tax_included = fields.Float(
        compute="_compute_standard_price_tax_included",
        string="Cost Price Tax Included",
        digits="Product Price",
        help="Cost Price of the product, All Tax Included:\n"
        "This field will be computed with the 'Cost Price', taking into"
        " account Sale Taxes setting.",
    )

    @api.depends_context("company")
    @api.depends(
        "product_variant_ids",
        "product_variant_ids.standard_price",
        "taxes_id",
        "taxes_id.price_include",
    )
    def _compute_standard_price_tax_included(self):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.standard_price_tax_included = (
                template.product_variant_ids.standard_price_tax_included
            )
        for template in self - unique_variants:
            template.standard_price_tax_included = 0.0
