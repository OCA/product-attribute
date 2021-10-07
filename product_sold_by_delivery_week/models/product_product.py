# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from babel.dates import DateTimeFormat

from odoo import api, fields, models
from odoo.tools import date_utils


class ProductProduct(models.Model):
    _inherit = "product.product"

    weekly_sold_delivered = fields.Char(
        company_dependent=True, groups="sales_team.group_sale_salesman",
    )
    weekly_sold_delivered_shown = fields.Char(
        string="Weekly Sold",
        compute="_compute_weekly_sold_delivered_shown",
        groups="sales_team.group_sale_salesman",
    )

    @api.depends("weekly_sold_delivered")
    def _compute_weekly_sold_delivered_shown(self):
        """This field is meant to be used only for display purposes so we can use custom
        characters show the sales stream. We want to keep the stored one as base 2
        string so we can perform bitwise operations easily"""
        params = self.env["ir.config_parameter"].sudo()
        sold_char = params.get_param("product_sold_by_delivery_week.sold_char", "●")
        not_sold_char = params.get_param(
            "product_sold_by_delivery_week.not_sold_char", "◌"
        )
        not_service_products = self.filtered(lambda x: x.type != "service")
        (self - not_service_products).weekly_sold_delivered_shown = False
        for product in self.filtered(lambda x: x.type != "service"):
            product.weekly_sold_delivered_shown = (
                product.weekly_sold_delivered
                and "".join(
                    [
                        int(c) and sold_char or not_sold_char
                        for c in product.weekly_sold_delivered
                    ]
                )
            )

    def _weekly_sold_delivered_domain(self, date_start, date_end):
        company_id = self.env.context.get("force_company", self.env.user.company_id.id)
        return [
            ("product_id", "in", self.ids),
            ("date", ">=", date_start),
            ("date", "<", date_end),
            ("state", "=", "done"),
            ("sale_line_id", "!=", False),
            ("picking_code", "=", "outgoing"),
            ("company_id", "=", company_id),
        ]

    def _recalculate_weekly_sold_delivered(self):
        """Over this recordset recalculate the whole strings. We end up with something
        like '010111'. Later we can transform it into something nicer for the user."""
        params = self.env["ir.config_parameter"].sudo()
        weeks_to_consider = params.get_param(
            "product_sold_by_delivery_week.weeks_to_consider", 6
        )
        company_id = self.env.context.get("force_company", self.env.user.company_id.id)
        delta_one_week = date_utils.get_timedelta(1, "week")
        start_of_this_week = date_utils.start_of(fields.Datetime.today(), "week")
        start_of_next_week = start_of_this_week + delta_one_week
        start_of_period = start_of_this_week - date_utils.get_timedelta(
            weeks_to_consider - 1, "week"
        )
        date_range = date_utils.date_range(
            start_of_period, start_of_next_week, delta_one_week
        )
        # We'll reuse this dictionary to obtain the final string
        week_dates_dict = {}
        for week_position in range(weeks_to_consider):
            locale_date = DateTimeFormat(
                next(date_range), locale=self.env.user.lang or "en_US"
            )
            week_dates_dict[week_position] = (
                int(locale_date["w"]),
                int(locale_date["y"]),
            )
        # Get all the results in a single query
        sold_grouped = self.env["stock.move"].read_group(
            self._weekly_sold_delivered_domain(start_of_period, start_of_next_week),
            ["date", "product_id"],
            ["date:week", "product_id"],
            lazy=False,
        )
        if not sold_grouped:
            self.with_context(force_company=company_id).write(
                {"weekly_sold_delivered": "0" * weeks_to_consider}
            )
            return
        weekly_product_ids = {}
        for date_product in sold_grouped:
            (int(date_product["date:week"][1:3]), int(date_product["date:week"][-4:]))
            week_year_tuple = (
                int(date_product["date:week"][1:3]),
                int(date_product["date:week"][-4:]),
            )
            weekly_product_ids.setdefault(week_year_tuple, [])
            weekly_product_ids[week_year_tuple].append(date_product["product_id"][0])
        # We'll get a dict like this
        # {
        #     product.product(1,): '000000',
        #     product.product(2,): '010110',
        #     product.product(3,): '000010',
        # }
        products_weekly = {}
        for product in self:
            products_weekly[product] = "".join(
                [
                    product.id in weekly_product_ids.get(w, []) and "1" or "0"
                    for p, w in week_dates_dict.items()
                ]
            )
        # But we want to group by string result so we can minimize the final records
        # writes. The number of writes will depends on the variety of the weekly sales
        # up to a maximum given by the parameter `weeks_to_consider` allows us in bits.
        # So for 8 weeks, a maximum of 256 writes would be made.
        weekly_result_dict = {}
        for product, weekly_string in products_weekly.items():
            weekly_result_dict.setdefault(weekly_string, self.env["product.product"])
            weekly_result_dict[weekly_string] |= product
        for weekly_string, product_recordset in weekly_result_dict.items():
            if not product_recordset:
                continue
            product_recordset.with_context(force_company=company_id).write(
                {"weekly_sold_delivered": weekly_string}
            )

    @api.model
    def _action_recalculate_all_weekly_sold_delivered(self):
        """To be launched by the cron or the init hook"""
        companies = self.env["res.company"].search([])
        for company in companies:
            products = (
                self.env["product.product"]
                .search(
                    [
                        ("type", "!=", "service"),
                        "|",
                        ("company_id", "=", company.id),
                        ("company_id", "=", False),
                    ]
                )
                .with_context(force_company=company.id)
            )
            if not products:
                continue
            products._recalculate_weekly_sold_delivered()
