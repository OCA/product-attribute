# Copyright 2026 Kreilabs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockForecastedProductProduct(models.AbstractModel):
    _inherit = "stock.forecasted_product_product"

    def _get_report_header(self, product_template_ids, product_ids, wh_location_ids):
        """Keep sale/purchase/mrp header data; hide on-hand value without cost ACL.

        stock_account sums stock.quant.value for stock managers. That field is
        restricted to group_product_cost. The value is computed as superuser so
        replenishment quantities from other modules still reach ForecastedDetails.
        """
        can_see_cost = self.env.user.has_group(
            "product_cost_security.group_product_cost"
        )
        if can_see_cost:
            return super()._get_report_header(
                product_template_ids, product_ids, wh_location_ids
            )
        res = super(
            StockForecastedProductProduct, self.sudo()
        )._get_report_header(product_template_ids, product_ids, wh_location_ids)
        res.pop("value", None)
        return res
