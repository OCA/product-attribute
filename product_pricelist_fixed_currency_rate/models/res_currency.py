# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductPricelist(models.Model):
    _inherit = "res.currency"

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        fixed_rate = self.env.context.get("fixed_currency_rate")
        if fixed_rate:
            return fixed_rate
        return super()._get_conversion_rate(from_currency, to_currency, company, date)
