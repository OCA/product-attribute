# Copyright 2023 FactorLibre - Hugo Córdoba
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class WizardPricelistSimulation(models.TransientModel):
    _inherit = "wizard.preview.pricelist"
    _description = "wizard - Preview Pricelist"

    standard_price = fields.Float(
        string="Cost",
    )

    def _set_standard_price(self):
        if self.template_id:
            self.standard_price = self.template_id.standard_price
        elif self.product_id:
            self.standard_price = self.product_id.standard_price

    def _get_product(self, pricelist):
        if self.template_id:
            product = self.template_id.with_context(
                quantity=self.product_qty,
                pricelist=pricelist.id,
                date=self.price_date,
            )
        elif self.product_id:
            product = self.product_id.with_context(
                quantity=self.product_qty,
                pricelist=pricelist.id,
                date=self.price_date,
            )
        return product

    def _prepare_simulation_lines_vals(self, variant, pricelist):
        rslt = super()._prepare_simulation_lines_vals(variant, pricelist)
        to_currency = pricelist.currency_id
        self._set_standard_price()
        product = self._get_product(pricelist)
        res = product.taxes_id.compute_all(
            rslt.get("price"),
            to_currency,
            self.product_qty,
            product=product,
        )
        price_vat_excl = res["total_excluded"] / self.product_qty
        price_vat_incl = res["total_included"] / self.product_qty

        cost = self.env.user.company_id.currency_id._convert(
            self.standard_price,
            to_currency,
            self.env.user.company_id,
            self.price_date,
            round=False,
        )
        rslt.update(
            {
                "price_vat_excl": price_vat_excl,
                "price_vat_incl": price_vat_incl,
                "margin": price_vat_excl - cost,
                "margin_percent": price_vat_excl
                and ((price_vat_excl - cost) / price_vat_excl) * 100,
            }
        )
        return rslt


class PricelistSimulationLine(models.TransientModel):
    _inherit = "wizard.preview.pricelist.line"
    _description = "wizard - Preview Pricelist Line"

    price_vat_excl = fields.Monetary(string="Unit Sales Price (Excl.)", readonly=True)
    price_vat_incl = fields.Monetary(string="Unit Sales Price (Incl.)", readonly=True)

    margin = fields.Monetary(
        store=True,
        digits="Price",
        readonly=True,
    )

    margin_percent = fields.Float(
        string="Margin (%)",
        store=True,
        digits="Price",
        readonly=True,
    )
