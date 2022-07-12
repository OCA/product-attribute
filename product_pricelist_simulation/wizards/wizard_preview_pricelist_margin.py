# Copyright (C) 2021-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class WizardPreviewPricelistMargin(models.TransientModel):
    _name = "wizard.preview.pricelist.margin"
    _description = "Wizard - Preview Pricelist Margin"

    template_id = fields.Many2one(
        comodel_name="product.template", string="Product",
        default=lambda x: x._default_template_id())

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Variant",
        default=lambda x: x._default_product_id(),
        domain="[('product_tmpl_id', '=', template_id)]",
        required=True)

    standard_price = fields.Float(
        string='Cost',
        digits=dp.get_precision('Product Price'),
        related="product_id.standard_price",
        readonly=True,
        groups="base.group_user")

    product_qty = fields.Float(
        string="Quantity",
        default=1,
        required=True)

    price_date = fields.Date(
        string="Date", default=fields.Date.context_today,
        required=True)

    line_ids = fields.One2many(
        comodel_name="wizard.preview.pricelist.margin.line", string="Lines",
        inverse_name="wizard_id", compute="_compute_line_ids",
        readonly=True)

    def _default_product_id(self):
        if self.env.context.get("active_model", False) == "product.product":
            return self.env.context.get("active_id", False)
        elif self.env.context.get("active_model", False) == "product.template":
            return self.env["product.template"].browse(
                self.env.context.get("active_id", False)
            ).mapped("product_variant_ids")[0].id

    def _default_template_id(self):
        if self.env.context.get("active_model", False) == "product.template":
            return self.env.context.get("active_id", False)

    def _get_pricelists(self):
        """Overload this function to filter pricelist to be displayed"""
        return self.env["product.pricelist"].search([])

    @api.depends("product_id", "product_qty", "price_date")
    def _compute_line_ids(self):
        pricelists = self._get_pricelists()
        lines_vals = []
        if not self.product_id or not self.product_qty:
            return
        for pricelist in pricelists:
            product = self.product_id.with_context(
                quantity=self.product_qty,
                pricelist=pricelist.id,
                date=self.price_date,
            )
            to_currency = pricelist.currency_id
            res = product.taxes_id.compute_all(
                product.price,
                to_currency,
                self.product_qty,
                product=product
            )

            price_vat_excl = res["total_excluded"] / self.product_qty
            price_vat_incl = res["total_included"] / self.product_qty

            cost = self.env.user.company_id.currency_id._convert(
                self.product_id.standard_price, to_currency,
                self.env.user.company_id,
                self.price_date,
                round=False)

            line_vals = {
                "pricelist_id": pricelist.id,
                "price_vat_excl": price_vat_excl,
                "price_vat_incl": price_vat_incl,
                "margin": price_vat_excl - cost,
                "margin_percent": price_vat_excl and (
                    (price_vat_excl - cost) / price_vat_excl
                ) * 100,
            }
            lines_vals.append((0, 0, line_vals))
        self.line_ids = lines_vals
