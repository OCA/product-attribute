# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class ABCClassificationProfile(models.Model):
    _name = "abc.classification.profile"
    _description = "ABC Classification Profile"

    name = fields.Char()
    level_ids = fields.One2many(
        comodel_name="abc.classification.profile.level", inverse_name="profile_id"
    )
    classification_type = fields.Selection(
        selection=[("percentage", "Percentage"), ("fixed", "Fixed")],
        default="percentage",
        required=True,
    )
    representation = fields.Char(compute="_compute_representation")
    data_source = fields.Selection(
        selection=[("stock_moves", "Stock Moves")],
        default="stock_moves",
        index=True,
        required=True,
    )
    value_criteria = fields.Selection(
        selection=[
            ("consumption_value", "Consumption Value"),
            ("sales_revenue", "Sales Revenue"),
            ("sales_volume", "Sales Volume"),
            # others: 'profitability', ...
        ],
        default="consumption_value",
        string="Value",
        index=True,
        required=True,
    )
    past_period = fields.Integer(
        default=365, string="Past demand period (Days)", required=True
    )
    days_to_ignore = fields.Integer(string="Ignore newer than these days")
    product_variant_ids = fields.One2many(
        "product.product", inverse_name="abc_classification_profile_id"
    )
    product_count = fields.Integer(compute="_compute_product_count", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company")

    @api.constrains("past_period", "days_to_ignore")
    def _check_period(self):
        for profile in self:
            if profile.days_to_ignore > profile.past_period:
                raise ValidationError(
                    _("The days to ignore can not be greater than the past period.")
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
            if profile.classification_type == "percentage":
                percentages = profile.level_ids.mapped("percentage")
                total = sum(percentages)
                if profile.level_ids and total != 100.0:
                    raise ValidationError(
                        _("The sum of the percentages of the levels should be 100.")
                    )

    @api.depends("product_variant_ids")
    def _compute_product_count(self):
        for profile in self:
            profile.product_count = len(profile.product_variant_ids)

    def action_view_products(self):
        products = self.mapped("product_variant_ids")
        action = self.env["ir.actions.act_window"].for_xml_id(
            "product", "product_variant_action"
        )
        del action["context"]
        if len(products) > 1:
            action["domain"] = [("id", "in", products.ids)]
        elif len(products) == 1:
            form_view = [
                (self.env.ref("product.product_variant_easy_edit_view").id, "form")
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = products.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    def _fill_initial_product_data(self, date, date_end=False):
        product_list = []
        if self.data_source == "stock_moves":
            return self._fill_data_from_stock_moves(
                date, product_list, date_end=date_end
            )
        else:
            return product_list

    def _fill_data_from_stock_moves(self, date, product_list, date_end=False):
        self.ensure_one()
        domain = [
            ("state", "=", "done"),
            ("date", ">=", date),
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
        ]
        if date_end:
            domain.append(("date", "<=", date_end))
        moves = (
            self.env["stock.move"]
            .sudo()
            .read_group(
                domain,
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
        elif self.value_criteria == "sales_revenue":
            return data["unit_price"] * data["units_sold"]
        elif self.value_criteria == "sales_volume":
            return data["units_sold"]
        return 0.0

    @api.model
    def _get_sort_key_percentage(self, rec):
        return rec.percentage

    @api.model
    def _get_sort_key_fixed(self, rec):
        return rec.fixed

    @api.model
    def _compute_abc_classification(self):
        def _get_sort_key_value(data):
            return data["value"]

        profiles = self.search([]).filtered(lambda p: p.level_ids)
        for profile in profiles:
            oldest_date = fields.Datetime.to_string(
                fields.Datetime.today() - timedelta(days=profile.past_period)
            )
            final_date = fields.Datetime.to_string(
                fields.Datetime.today() - timedelta(days=profile.days_to_ignore)
            )
            totals = {
                "units_sold": 0,
                "value": 0.0,
            }
            product_list = profile._fill_initial_product_data(oldest_date, final_date)
            for product_data in product_list:
                product_data["unit_cost"] = product_data["product"].standard_price
                product_data["unit_price"] = product_data["product"].list_price
                totals["units_sold"] += product_data["units_sold"]
                product_data["value"] = profile._get_inventory_product_value(
                    product_data
                )
                totals["value"] += product_data["value"]
            product_list.sort(reverse=True, key=_get_sort_key_value)
            levels = profile.level_ids.sorted(
                key=getattr(self, "_get_sort_key_%s" % profile.classification_type),
                reverse=True,
            )
            if profile.classification_type == "percentage":
                level_percentage = [[level, level.percentage] for level in levels]
                current_value = 0
                accumulated_percentage = level_percentage[0][1]
                for product_data in product_list:
                    # Accumulated current value
                    current_value += product_data["value"] or 0.0
                    # This comparison would be the same as:
                    # current_value * 100 / totals["value"] > accumulated_percentage,
                    # but it is written in the next way to avoid division and decimal lost.
                    while (
                        current_value * 100 > accumulated_percentage * totals["value"]
                        and len(level_percentage) > 1
                    ):
                        level_percentage.pop(0)
                        accumulated_percentage += level_percentage[0][1]
                    product_data[
                        "product"
                    ].abc_classification_level_id = level_percentage[0][0]
            elif profile.classification_type == "fixed":
                if product_list:
                    zero_level = profile.level_ids.filtered(
                        lambda l: float_is_zero(l.fixed, precision_digits=2)
                    )
                    self.env["product.product"].search(
                        [("abc_classification_profile_id", "=", profile.id)]
                    ).write({"abc_classification_level_id": zero_level.id})
                    current_value = 0
                    for product_data in product_list:
                        level_fixed = [[level, level.fixed] for level in levels]
                        fixed_value = level_fixed[0][1]
                        current_value = product_data["value"] or 0.0
                        while current_value < fixed_value and len(level_fixed) > 1:
                            level_fixed.pop(0)
                            fixed_value = level_fixed[0][1]
                        product_data[
                            "product"
                        ].abc_classification_level_id = level_fixed[0][0]
