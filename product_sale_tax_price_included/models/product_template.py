# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    _SALE_TAX_PRICE_INCLUDE_SELECTION = [
        ("no_tax", "No sale tax"),
        ("all_tax_excl", "Taxes are not included in sale price"),
        ("all_tax_incl", "All taxes are included in sale price"),
        ("various_taxes", "Sale price may include taxes"),
    ]

    sale_tax_price_include = fields.Selection(
        selection=_SALE_TAX_PRICE_INCLUDE_SELECTION,
        compute="_compute_sale_tax_price_include",
        string="Taxes in Sale Price",
        help="Indicate if the Sale Price include Taxes or not",
    )

    price_vat_excl = fields.Float(
        compute="_compute_price_vat_incl_excl",
        string="Sales Price (Excl.)",
        help="Sale Price, All Taxes Excluded"
    )
    price_vat_incl = fields.Float(
        compute="_compute_price_vat_incl_excl",
        string="Sales Price (Incl.)",
        help="Sale Price, All Taxes Included"
    )

    @api.multi
    @api.depends(
        "list_price", "taxes_id", "taxes_id.amount_type", "taxes_id.amount",
        "taxes_id.include_base_amount")
    def _compute_price_vat_incl_excl(self):
        for template in self:
            info = template.taxes_id.compute_all(
                template.list_price, quantity=1.0)
            template.price_vat_excl = info["total_excluded"]
            template.price_vat_incl = info["total_included"]

    @api.multi
    @api.depends("taxes_id", "taxes_id.price_include")
    def _compute_sale_tax_price_include(self):
        for template in self:
            price_includes = template.mapped('taxes_id.price_include')

            if not len(price_includes):
                template.sale_tax_price_include = "no_tax"
            elif all(price_includes):
                template.sale_tax_price_include = "all_tax_incl"
            elif any(price_includes) and len(price_includes) > 1:
                template.sale_tax_price_include = "various_taxes"
            else:
                template.sale_tax_price_include = "all_tax_excl"
