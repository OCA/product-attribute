# Copyright (C) 2026 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expiration_time_months = fields.Float(
        string="Expiration Time (Months)",
        compute="_compute_expiration_time_months",
        inverse="_inverse_expiration_time_months",
        store=True,
        help="Expiration time in months (can be fractional). Will be converted "
        "to days using the system parameter "
        "'product_expiry_month.days_per_year'.",
    )

    @api.depends("expiration_time")
    def _compute_expiration_time_months(self):
        if self:
            days_per_year = float(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("product_expiry_month.days_per_year", "365")
            )
        for template in self:
            template.expiration_time_months = (
                template.expiration_time * 12 / days_per_year
            )

    def _inverse_expiration_time_months(self):
        if self:
            days_per_year = float(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("product_expiry_month.days_per_year", "365")
            )
        for template in self:
            template.expiration_time = round(
                template.expiration_time_months * days_per_year / 12
            )
