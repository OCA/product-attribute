# Copyright 2020 ForgeFlow S.L.(http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

import numpy as np

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    variability_profile_categ_id = fields.Many2one("variability.profile")


class ProductProduct(models.Model):
    _inherit = "product.product"

    variability_profile_id = fields.Many2one(comodel_name="variability.profile")

    demand_class_id = fields.Many2one("variability.profile.class", readonly=True)
    variability_factor = fields.Float(readonly=True)

    def _past_moves_domain(self, date_from, date_to, product_id):
        self.ensure_one()
        return [
            ("state", "=", "done"),
            ("location_id.usage", "!=", "customer"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "=", product_id),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
        ]

    def _calc_past_demand(self, profile_horizon_past, profile_source, product_id):
        self.ensure_one()
        qty = []
        total_qty = 0.0
        horizon = profile_horizon_past
        date_from = fields.Date.to_string(datetime.now() + timedelta(days=-horizon))
        date_to = fields.Date.to_string(datetime.now())
        domain = self._past_moves_domain(date_from, date_to, product_id)
        moves = (
            self.env["stock.move"]
            .sudo()
            .read_group(domain, ["product_id", "product_qty"], ["product_id"],)
        )
        for group in moves:
            total_qty += group["product_qty"]
        for move in self.env["stock.move"].search(domain):
            qty.append(move["product_qty"])
        return {"qty": qty, "total_qty": total_qty}

    def cron_update_class(self):
        products = self.search(
            [
                "|",
                ("variability_profile_id", "!=", False),
                ("categ_id.variability_profile_categ_id", "!=", False),
            ]
        )
        for product in products:
            profile = (
                product.variability_profile_id
                or product.categ_id.variability_profile_categ_id
            )
            past_demand = product._calc_past_demand(
                profile.profile_horizon_past, profile.profile_source, product.id
            )
            if past_demand["qty"]:
                standard_deviation = np.std(past_demand["qty"])
                product.variability_factor = (
                    standard_deviation / past_demand["total_qty"]
                )
                for demand_class in profile.demand_class_ids:
                    if (
                        demand_class.lower_range
                        <= product.variability_factor
                        <= demand_class.upper_range
                    ):
                        product.demand_class_id = demand_class
