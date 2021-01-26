# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AbcClassificationProfile(models.Model):

    _inherit = "abc.classification.profile"

    profile_type = fields.Selection(selection_add=[("stock", "Stock")])

    def _fill_initial_product_data(self, date):
        product_list = []
        if self.profile_type == "stock":
            return self._fill_data(date, product_list)
        return product_list, 0

    def _fill_data(self, date, product_list):
        self.ensure_one()
        warehouse = self.env.ref("stock.warehouse0")
        self.env.cr.execute(
            """ SELECT sol.product_id product_id, so.warehouse_id warehouse_id, COUNT(sol.id) number_of_so_lines
                    FROM
                        sale_order so
                    JOIN
                        sale_order_line sol ON sol.order_id = so.id
                    JOIN
                        stock_move sm ON sol.id = sm.order_line_id
                    JOIN
                        abc_classification_profile_product_rel rel ON rel.product_id = sol.product_id
                    WHERE sol.qty_delivered > 0
                        AND sm.date > %(start_date)s
                        AND rel.profile_id = %(profile_id)s
                    GROUP BY so.warehouse_id, sol.product_id
                    ORDER BY number_of_so_lines DESC
        """,
            {
                "start_date": date,
                "current_warehouse_id": warehouse.id,
                "profile_id": self.id,
            },
        )

        result = self.env.cr.fetchall()
        total = 0
        for r in result:
            product_data = {
                "product": self.env["product.product"].browse(r[0]),
                "warehouse": self.env["stock.warehouse"].browse(r[1]),
                "number_of_so_lines": int(r[2]),
            }
            total += int(r[2])
            product_list.append(product_data)
        return product_list, total

    @api.model
    def _compute_abc_classification(self):
        def _get_sort_key_value(data):
            return data["number_of_so_lines"]

        def _get_sort_key_percentage(rec):
            return rec.percentage

        profiles = self.search([]).filtered(lambda p: p.level_ids)

        ProductClassification = self.env["abc.classification.product.level"]

        for profile in profiles:
            start_date = fields.Datetime.to_string(
                datetime.today() - timedelta(days=profile.period)
            )

            product_list, total = profile._fill_initial_product_data(start_date)

            levels = profile.level_ids.sorted(
                key=_get_sort_key_percentage, reverse=True
            )
            percentages = levels.mapped("percentage")
            cum_percentages = []
            previous_percentage = None
            for i, perc in enumerate(percentages):
                if i == 0:
                    percentage_to_append = perc
                    cum_percentages.append(percentage_to_append)
                else:
                    percentage_to_append = previous_percentage + perc
                    cum_percentages.append(percentage_to_append)
                previous_percentage = percentage_to_append

            level_percentage = list(zip(levels, cum_percentages))

            level, percentage = level_percentage.pop(0)
            previous_data = {}
            for i, product_data in enumerate(product_list):

                # Compute percentages and cumulative percentages for the products
                product_data["number_of_so_lines_percentage"] = (
                    (100.0 * product_data["number_of_so_lines"] / total)
                    if total
                    else 0.0
                )

                product_data["cumulative_percentage"] = (
                    product_data["number_of_so_lines_percentage"]
                    if i == 0
                    else (
                        product_data["number_of_so_lines_percentage"]
                        + previous_data["cumulative_percentage"]
                    )
                )
                if product_data["cumulative_percentage"] > 100:
                    raise UserError(_("Cumulative percentage greater than 100."))

                # Compute ABC classification for the products based on the cumulative percentage

                if (
                    product_data["cumulative_percentage"] > percentage
                    and len(level_percentage) > 0
                ):
                    level, percentage = level_percentage.pop(0)

                product_abc_classification = product_data[
                    "product"
                ].abc_product_classification_level_ids.filtered(
                    lambda p, profile: p.profile_id == profile.id
                )

                if product_abc_classification:
                    product_abc_classification.write({"computed_level_id": level.id})
                else:
                    product_abc_classification = ProductClassification.create(
                        {
                            "product_id": product_data["product"].id,
                            "profile_id": profile.id,
                            "computed_level_id": level.id,
                        }
                    )

                previous_data = product_data
