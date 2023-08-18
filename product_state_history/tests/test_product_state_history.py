# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import mock

from odoo import fields

from .common import CommonProductStateHistory


class TestProductStateHistory(CommonProductStateHistory):
    def test_history(self):
        with mock.patch.object(fields.Datetime, "now") as mock_now:
            mock_now.return_value = "2020-07-29 13:00:00"
            self.product_1.state = "end"
        history = self.history_obj.search(
            [("product_template_id", "=", self.product_1.id)],
            limit=1,
        )
        self.assertEqual(
            fields.Datetime.from_string("2020-07-29 13:00:00"),
            history.state_date,
        )
        self.assertEqual(
            self.end,
            history.product_state_id,
        )

        with mock.patch.object(fields.Datetime, "now") as mock_now:
            mock_now.return_value = "2020-07-29 14:00:00"
            self.product_1.state = "obsolete"

        history = self.history_obj.search(
            [("product_template_id", "=", self.product_1.id)],
            limit=1,
        )
        self.assertEqual(
            fields.Datetime.from_string("2020-07-29 14:00:00"),
            history.state_date,
        )
        self.assertEqual(
            self.obsolete,
            history.product_state_id,
        )

        with mock.patch.object(fields.Datetime, "now") as mock_now:
            mock_now.return_value = "2020-07-29 15:00:00"
            self.product_2.state = "end"
        history = self.history_obj.search(
            [("product_template_id", "=", self.product_2.id)],
            limit=1,
        )
        self.assertEqual(
            fields.Datetime.from_string("2020-07-29 15:00:00"),
            history.state_date,
        )
        self.assertEqual(
            self.end,
            history.product_state_id,
        )

        result = self.product_2.product_tmpl_id.action_product_state_history()
        self.assertIn(
            ("product_template_id", "in", [self.product_2.product_tmpl_id.id]),
            result["domain"],
        )

    def test_history_wizard(self):
        # Set Product to End of Life
        # Launch report with pivot date > and state == End of Life
        # Should find product
        # Then launch report with pivot date <
        # Should return nothing
        # Then, set back to Normal (e.g.: if user did it wrong way)
        # Should return nothing
        with mock.patch.object(fields.Datetime, "now") as mock_now:
            mock_now.return_value = "2020-07-29 13:00:00"
            self.product_1.state = "end"
        history = self.history_obj.search(
            [("product_template_id", "=", self.product_1.id)],
            limit=1,
        )
        vals = {"product_state_id": self.end.id, "pivot_date": "2020-07-29 14:00"}
        report = self.history_wizard_obj.create(vals).print_report()

        self.assertEqual(
            report["data"]["ids"],
            [],
        )
        vals = {"product_state_id": self.end.id, "pivot_date": "2020-07-29 12:00"}
        report = self.history_wizard_obj.create(vals).print_report()
        self.assertEqual(
            report["data"]["ids"],
            history.ids,
        )

        with mock.patch.object(fields.Datetime, "now") as mock_now:
            mock_now.return_value = "2020-07-29 14:00:00"
            self.product_1.state = "sellable"

        vals = {"product_state_id": self.end.id, "pivot_date": "2020-07-29 15:00:00"}
        report = self.history_wizard_obj.create(vals).print_report()
        self.assertEqual(
            report["data"]["ids"],
            [],
        )
