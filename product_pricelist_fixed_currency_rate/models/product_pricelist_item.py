# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist.item"

    fixed_currency_rate = fields.Float(
        digits=(12, 12),
        help="If set (different to 0.0), the currency conversion will "
        "ignore the actual currency rate and always use the fixed "
        "currency rate.",
    )
    inverse_fixed_currency_rate = fields.Float(
        digits=(12, 12),
        compute="_compute_inverse_fixed_currency_rate",
        inverse="_inverse_inverse_fixed_currency_rate",
        help="If set (different to 0.0), the currency conversion will "
        "ignore the actual currency rate and always use the fixed "
        "currency rate.",
    )
    is_fixed_currency_rate_applicable = fields.Boolean(
        compute="_compute_is_fixed_currency_rate_applicable"
    )
    actual_currency_rate = fields.Float(
        digits=(12, 12), compute="_compute_is_fixed_currency_rate_applicable"
    )
    inverse_actual_currency_rate = fields.Float(
        digits=(12, 12), compute="_compute_is_fixed_currency_rate_applicable"
    )
    do_inverse_currency_rate = fields.Boolean(
        compute="_compute_do_inverse_currency_rate",
        store=True,
        readonly=False,
    )
    currency_rate_tooltip = fields.Char(
        compute="_compute_currency_rate_tooltip",
    )

    @api.depends("base_pricelist_id", "base_pricelist_id.currency_id", "base")
    def _compute_is_fixed_currency_rate_applicable(self):
        for rec in self:
            applicable = (
                rec.base == "pricelist"
                and rec.base_pricelist_id
                and rec.base_pricelist_id.currency_id != rec.pricelist_id.currency_id
            )
            rec.is_fixed_currency_rate_applicable = applicable
            if applicable:
                curr_from = rec.base_pricelist_id.currency_id
                curr_to = rec.pricelist_id.currency_id
                company = rec.company_id or self.env.company
                rate = self.env["res.currency"]._get_conversion_rate(
                    curr_from, curr_to, company, rec.date_end or fields.Date.today()
                )
                rec.actual_currency_rate = rate
                rec.inverse_actual_currency_rate = 1 / rate if rate else 0.0
            else:
                rec.actual_currency_rate = 1.0
                rec.inverse_actual_currency_rate = 1.0

    def _compute_base_price(self, product, quantity, uom, date, target_currency):
        if self.is_fixed_currency_rate_applicable and self.fixed_currency_rate:
            return super(
                ProductPricelist,
                self.with_context(fixed_currency_rate=self.fixed_currency_rate),
            )._compute_base_price(product, quantity, uom, date, target_currency)
        return super()._compute_base_price(
            product, quantity, uom, date, target_currency
        )

    @api.depends("base_pricelist_id", "base_pricelist_id.currency_id")
    def _compute_do_inverse_currency_rate(self):
        for rec in self:
            if rec.is_fixed_currency_rate_applicable:
                rec.do_inverse_currency_rate = rec.actual_currency_rate < 1.0

    @api.depends("do_inverse_currency_rate")
    def _compute_currency_rate_tooltip(self):
        for rec in self:
            if rec.do_inverse_currency_rate:
                curr_from = rec.pricelist_id.currency_id
                curr_to = rec.base_pricelist_id.currency_id
            else:
                curr_from = rec.base_pricelist_id.currency_id
                curr_to = rec.pricelist_id.currency_id
            rec.currency_rate_tooltip = _("({curr_from} to {curr_to} rates)").format(
                curr_from=curr_from.name, curr_to=curr_to.name
            )

    @api.depends("fixed_currency_rate")
    def _compute_inverse_fixed_currency_rate(self):
        for rec in self:
            rec.inverse_fixed_currency_rate = (
                1 / rec.fixed_currency_rate if rec.fixed_currency_rate else 0.0
            )

    def _inverse_inverse_fixed_currency_rate(self):
        for rec in self:
            rec.fixed_currency_rate = (
                1 / rec.inverse_fixed_currency_rate
                if rec.inverse_fixed_currency_rate
                else 0.0
            )

    def toggle_do_inverse_currency_rate(self):
        for rec in self:
            rec.do_inverse_currency_rate = not rec.do_inverse_currency_rate
