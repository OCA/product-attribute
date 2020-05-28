# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ABCClasificationProfile(models.Model):
    _name = "abc.classification.profile"
    _description = "ABC Clasification Profile"

    name = fields.Char()
    level_ids = fields.One2many(
        comodel_name="abc.classification.profile.level", inverse_name="profile_id"
    )
    representation = fields.Char(compute="_compute_representation")
    data_source = fields.Selection(
        selection=[("stock_moves", "Stock Moves")],
        default="stock_moves",
        string="Data Source",
        index=True,
        required=True,
    )
    value_criteria = fields.Selection(
        selection=[("consumption_value", "Consumption Value")],
        # others: 'sales revenue', 'profitability', ...
        default="consumption_value",
        string="Value",
        index=True,
        required=True,
    )
    past_period = fields.Integer(
        default=365, string="Past demand period (Days)", required=True
    )

    @api.depends("level_ids")
    def _compute_representation(self):
        def _get_sort_key_percentage(rec):
            return rec.percentage

        for profile in self:
            profile.level_ids.sorted(key=_get_sort_key_percentage, reverse=True)
            profile.representation = "/".join(
                [str(x) for x in profile.level_ids.mapped("display_name")]
            )

    @api.constrains("level_ids")
    def _check_levels(self):
        for profile in self:
            percentages = profile.level_ids.mapped("percentage")
            total = sum(percentages)
            if profile.level_ids and total != 100.0:
                raise ValidationError(
                    _("The sum of the percentages of the levels should be 100.")
                )
            if profile.level_ids and len({}.fromkeys(percentages)) != len(percentages):
                raise ValidationError(
                    _("The percentages of the levels must be unique.")
                )

    def write(self, vals):
        return super().write(vals)

    def _fill_initial_product_data(self, date):
        product_list = []
        if self.data_source == "stock_moves":
            return self._fill_data_from_stock_moves(date, product_list)
        else:
            return product_list

    def _fill_data_from_stock_moves(self, date, product_list):
        self.ensure_one()
        moves = (
            self.env["stock.move"]
            .sudo()
            .read_group(
                [
                    ("state", "=", "done"),
                    ("date", ">", date),
                    ("location_dest_id.usage", "=", "customer"),
                    ("location_id.usage", "!=", "customer"),
                    ("product_id.type", "=", "product"),
                    "|",
                    ("product_id.abc_classification_profile_id", "=", self.id),
                    "|",
                    ("product_id.categ_id.abc_classification_profile_id", "=", self.id),
                    (
                        "product_id.categ_id.parent_id.abc_classification_profile_id",
                        "=",
                        self.id,
                    ),
                ],
                ["product_id", "product_qty"],
                ["product_id"],
            )
        )
        for move in moves:
            product_data = {
                "product": self.env["product.product"].browse(move["product_id"][0]),
                "units_sold": move["product_qty"],
            }
            product_list.append(product_data)
        return product_list

    def _get_inventory_product_value(self, data):
        self.ensure_one()
        if self.value_criteria == "consumption_value":
            return data["unit_cost"] * data["units_sold"]
        raise 0.0

    @api.model
    def _compute_abc_classification(self):
        def _get_sort_key_value(data):
            return data["value"]

        def _get_sort_key_percentage(rec):
            return rec.percentage

        profiles = self.search([]).filtered(lambda p: p.level_ids)
        for profile in profiles:
            oldest_date = fields.Datetime.to_string(
                fields.Datetime.today() - timedelta(days=profile.past_period)
            )
            totals = {
                "units_sold": 0,
                "value": 0.0,
            }
            product_list = profile._fill_initial_product_data(oldest_date)
            for product_data in product_list:
                product_data["unit_cost"] = product_data["product"].standard_price
                totals["units_sold"] += product_data["units_sold"]
                product_data["value"] = profile._get_inventory_product_value(
                    product_data
                )
                totals["value"] += product_data["value"]
            product_list.sort(reverse=True, key=_get_sort_key_value)
            levels = profile.level_ids.sorted(
                key=_get_sort_key_percentage, reverse=True
            )
            percentages = levels.mapped("percentage")
            level_percentage = list(zip(levels, percentages))
            for product_data in product_list:
                product_data["value_percentage"] = (
                    (100.0 * product_data["value"] / totals["value"])
                    if totals["value"]
                    else 0.0
                )
                while (
                    product_data["value_percentage"] < level_percentage[0][1]
                    and len(level_percentage) > 1
                ):
                    level_percentage.pop(0)
                product_data["product"].abc_classification_level_id = level_percentage[
                    0
                ][0]
