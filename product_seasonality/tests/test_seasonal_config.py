# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import exceptions

from .common import CommonCaseWithLines


class TestSeasonalityCase(CommonCaseWithLines):
    def _test_conf_line(self, line, date_ok, date_ko):
        for dt in date_ok:
            self.assertTrue(line.is_sale_ok(dt), f"{dt.strftime('%Y-%m-%d')} is wrong")
        for dt in date_ko:
            self.assertFalse(line.is_sale_ok(dt), f"{dt.strftime('%Y-%m-%d')} is wrong")

    def test_display_name_with_variant(self):
        line = self.seasonal_conf.config_for_product(self.prod1)
        self.assertEqual(
            line.display_name,
            f"[{self.seasonal_conf.display_name}] {self.prod1.display_name} ({line.id})",
        )

    def test_display_name_with_template_only(self):
        line = self.seasonal_conf.config_for_product(self.prod1)
        line.product_id = False
        tmpl = line.product_template_id
        self.assertEqual(
            line.display_name,
            f"[{self.seasonal_conf.display_name}] {tmpl.display_name} ({line.id})",
        )

    def test_constraint(self):
        line = self.seasonal_conf.config_for_product(self.prod1)
        with self.assertRaisesRegex(
            exceptions.ValidationError,
            "The end date cannot be earlier than the start date.",
        ):
            line.date_end = datetime.datetime(2021, 5, 9)

    def test_config1(self):
        # line 1
        date_ok = (
            datetime.datetime(2021, 5, 10),  # mon
            datetime.datetime(2021, 5, 11),  # tue
            datetime.datetime(2021, 5, 12),  # wed
        )
        date_ko = (
            datetime.datetime(2021, 5, 5),  # out-of-range
            datetime.datetime(2021, 5, 13),  # thu
            datetime.datetime(2021, 5, 14),  # fri
            datetime.datetime(2021, 5, 15),  # sat
            datetime.datetime(2021, 5, 16),  # sun
            datetime.datetime(2021, 5, 18),  # out-of-range
        )
        line = self.seasonal_conf.config_for_product(self.prod1)
        self._test_conf_line(line, date_ok, date_ko)

    def test_config2(self):
        # line 2
        date_ok = (
            datetime.datetime(2021, 5, 13),  # thu
            datetime.datetime(2021, 5, 14),  # fri
            datetime.datetime(2021, 5, 15),  # sat
            datetime.datetime(2021, 5, 16),  # sun
            datetime.datetime(2021, 5, 20),  # thu
            datetime.datetime(2021, 5, 21),  # fri
            datetime.datetime(2021, 5, 22),  # sat
            datetime.datetime(2021, 5, 23),  # sun
        )
        date_ko = (
            datetime.datetime(2021, 5, 11),  # out-of-range
            datetime.datetime(2021, 5, 12),  # wed
            datetime.datetime(2021, 5, 17),  # mon
            datetime.datetime(2021, 5, 18),  # tue
            datetime.datetime(2021, 5, 19),  # wed
            datetime.datetime(2021, 5, 24),  # out-of-range
        )
        line = self.seasonal_conf.config_for_product(self.prod2)
        self._test_conf_line(line, date_ok, date_ko)
