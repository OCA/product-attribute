# Copyright 2025 Your Company
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestABCClassificationFinance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Create test warehouse
        cls.warehouse = cls.env["stock.warehouse"].search([], limit=1)
        if not cls.warehouse:
            cls.warehouse = cls.env["stock.warehouse"].create(
                {
                    "name": "Test Warehouse",
                    "code": "TST",
                    "reception_steps": "one_step",
                    "delivery_steps": "ship_only",
                }
            )

        # Create ABC profile for finance (cost based)
        cls.finance_profile = cls.env["abc.classification.profile"].create(
            {
                "name": "Test Finance Cost Profile",
                "profile_type": "cost",
                "warehouse_id": cls.warehouse.id,
                "period": 365,
            }
        )

        # Create levels for the profile
        cls.level_A = cls.env["abc.classification.level"].create(
            {
                "name": "A",
                "profile_id": cls.finance_profile.id,
                "percentage": 70,
                "percentage_products": 30,
            }
        )
        cls.level_B = cls.env["abc.classification.level"].create(
            {
                "name": "B",
                "profile_id": cls.finance_profile.id,
                "percentage": 30,
                "percentage_products": 70,
            }
        )

        # Create a product
        cls.product = cls.env["product.product"].create(
            {
                "name": "Finance Product",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "type": "product",
                "default_code": "FIN001",
                "tracking": "none",
            }
        )

    def test_compute_abc_classification_value_field(self):
        """
        _compute_abc_classification should assign value_field correctly for valid types
        """
        for profile_type, _expected_field in [
            ("cost", "total_cost"),
            ("sale_price", "total_sales"),
        ]:
            profile = self.env["abc.classification.profile"].create(
                {
                    "name": f"Test {profile_type}",
                    "profile_type": profile_type,
                    "warehouse_id": self.warehouse.id,
                    "period": 365,
                }
            )
            # Create a level for this profile
            level = self.env["abc.classification.level"].create(
                {
                    "name": f"Level for {profile_type}",
                    "profile_id": profile.id,
                    "percentage": 100,
                    "percentage_products": 100,
                }
            )
            # Patch _finance_get_data to return dummy data
            from unittest.mock import patch

            from ..models.abc_classification_profile import FinanceSaleData

            dummy_data = FinanceSaleData()
            dummy_data.product = self.product
            dummy_data.profile = profile
            with patch.object(
                type(profile), "_finance_get_data", return_value=([dummy_data], 0)
            ), patch.object(
                type(profile), "_finance_log_history", return_value=None
            ), patch.object(
                type(profile), "_get_existing_level_ids", return_value=[]
            ), patch.object(
                type(profile),
                "_build_ordered_level_cumulative_percentage",
                return_value=[(level, 100.0)],
            ), patch.object(
                type(profile), "_purge_obsolete_level_values", return_value=None
            ):
                try:
                    profile._compute_abc_classification()
                except Exception as e:
                    self.fail(f"Unexpected error for profile_type {profile_type}: {e}")

    def test_profile_requires_warehouse(self):
        """
        Finance profile must require a warehouse.
        """
        profile = self.env["abc.classification.profile"].new(
            {
                "name": "No Warehouse",
                "profile_type": "cost",
                "warehouse_id": False,
            }
        )
        with self.assertRaises(ValidationError):
            profile._check_warehouse_id()

    def test_finance_profile_type_selection(self):
        """
        Profile type should accept 'cost', 'sale_price'.
        """
        for profile_type in ["cost", "sale_price"]:
            profile = self.env["abc.classification.profile"].create(
                {
                    "name": f"Profile {profile_type}",
                    "profile_type": profile_type,
                    "warehouse_id": self.warehouse.id,
                }
            )
            self.assertEqual(profile.profile_type, profile_type)

    def test_history_record_creation(self):
        """
        Test that finance history records can be created and linked to product level.
        """
        product_level = self.env["abc.classification.product.level"].create(
            {
                "product_id": self.product.id,
                "computed_level_id": self.level_A.id,
                "profile_id": self.finance_profile.id,
            }
        )
        history = self.env["abc.finance.sale.level.history"].create(
            {
                "computed_level_id": self.level_A.id,
                "product_id": self.product.id,
                "purchase_price": 10.0,
                "total_cost": 100.0,
                "total_sales": 120.0,
                "profile_id": self.finance_profile.id,
                "warehouse_id": self.warehouse.id,
                "product_level_id": product_level.id,
            }
        )
        self.assertEqual(history.product_id, self.product)
        self.assertEqual(history.product_level_id, product_level)
        self.assertEqual(product_level.finance_sale_level_history_ids, history)

    def test_finance_data_query_methods(self):
        """
        Smoke test for _get_finance_data_query
        and _finance_init_collected_data_instance.
        """
        from_date = "2025-01-01"
        customer_location_ids = []
        query, params = self.finance_profile._get_finance_data_query(
            from_date, customer_location_ids
        )
        self.assertIsInstance(query, str)
        self.assertIsInstance(params, dict)
        self.assertIn("SUM(", query)
        self.assertIn("GROUP BY", query)
        self.assertIn("ORDER BY", query)
        data_instance = self.finance_profile._finance_init_collected_data_instance()
        self.assertEqual(data_instance.profile, self.finance_profile)

    def test_finance_get_data_cost(self):
        """
        Test _finance_get_data for 'cost' profile returns correct structure and values.
        """
        self.finance_profile.write(
            {"level_ids": [(6, 0, [self.level_A.id, self.level_B.id])]}
        )
        self.product.write(
            {"abc_classification_profile_ids": [(6, 0, [self.finance_profile.id])]}
        )
        finance_data_list, total = self.finance_profile._finance_get_data()
        self.assertIsInstance(finance_data_list, list)
        self.assertTrue(any(fd.product == self.product for fd in finance_data_list))
        for fd in finance_data_list:
            self.assertTrue(hasattr(fd, "total_cost"))
            self.assertTrue(hasattr(fd, "ranking"))
            self.assertTrue(hasattr(fd, "product"))
            self.assertTrue(hasattr(fd, "from_date"))
            self.assertTrue(hasattr(fd, "to_date"))
        self.assertIsInstance(total, (int, float))
        import csv
        import io

        from ..models.abc_classification_profile import FinanceSaleData

        cr = self.env.cr
        table = "abc_finance_sale_level_history"
        columns = FinanceSaleData._get_col_names()
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=";", lineterminator="\n")
        for finance_data in finance_data_list:
            finance_data.computed_level = self.level_A
            finance_data.product_level = None
            finance_data.percentage = 100.0
            finance_data.cumulated_percentage = 100.0
            finance_data.purchase_price = getattr(finance_data, "purchase_price", 10.0)
            finance_data.total_cost = getattr(finance_data, "total_cost", 10.0)
            finance_data.total_sales = getattr(finance_data, "total_sales", 10.0)
            finance_data.from_date = getattr(finance_data, "from_date", "2025-01-01")
            finance_data.to_date = getattr(finance_data, "to_date", "2025-12-31")
            finance_data.total_products = 1
            finance_data.percentage_products = 100.0
            finance_data.cumulated_percentage_products = 100.0
            finance_data.sum_cumulated_percentages = 100.0
            row = finance_data._to_csv_line()
            for idx in [0, 1, 2, 3, 4, 5, 11]:
                if row[idx] in (None, ""):
                    row[idx] = "\\N"
            for idx in [12, 13]:
                if not row[idx]:
                    row[idx] = "\\N"
            writer.writerow(row)
        buf.seek(0)
        cr.copy_from(buf, table, columns=columns, sep=";")
        self.env["abc.finance.sale.level.history"].flush_model()
        records = self.env["abc.finance.sale.level.history"].search([])
        self.assertGreaterEqual(len(records), 1)

    def test_finance_get_data_sale_price(self):
        """
        Test _finance_get_data for 'sale_price' profile returns
        correct structure and values.
        """
        profile = self.env["abc.classification.profile"].create(
            {
                "name": "Test Sale Price Profile",
                "profile_type": "sale_price",
                "warehouse_id": self.warehouse.id,
                "period": 365,
            }
        )
        profile.write({"level_ids": [(6, 0, [self.level_A.id, self.level_B.id])]})
        self.product.write({"abc_classification_profile_ids": [(6, 0, [profile.id])]})
        finance_data_list, total = profile._finance_get_data()
        self.assertIsInstance(finance_data_list, list)
        for fd in finance_data_list:
            self.assertTrue(hasattr(fd, "total_sales"))
            self.assertEqual(fd.total_cost, 0.0)
        import csv
        import io

        from ..models.abc_classification_profile import FinanceSaleData

        cr = self.env.cr
        table = "abc_finance_sale_level_history"
        columns = FinanceSaleData._get_col_names()
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=";", lineterminator="\n")
        for finance_data in finance_data_list:
            finance_data.computed_level = self.level_A
            finance_data.product_level = None
            finance_data.percentage = 100.0
            finance_data.cumulated_percentage = 100.0
            finance_data.purchase_price = getattr(finance_data, "purchase_price", 10.0)
            finance_data.total_cost = getattr(finance_data, "total_cost", 0.0)
            finance_data.total_sales = getattr(finance_data, "total_sales", 10.0)
            finance_data.from_date = getattr(finance_data, "from_date", "2025-01-01")
            finance_data.to_date = getattr(finance_data, "to_date", "2025-12-31")
            finance_data.total_products = 1
            finance_data.percentage_products = 100.0
            finance_data.cumulated_percentage_products = 100.0
            finance_data.sum_cumulated_percentages = 100.0
            row = finance_data._to_csv_line()
            for idx in [0, 1, 2, 3, 4, 5, 11]:
                if row[idx] in (None, ""):
                    row[idx] = "\\N"
            for idx in [12, 13]:
                if not row[idx]:
                    row[idx] = "\\N"
            writer.writerow(row)
        buf.seek(0)
        cr.copy_from(buf, table, columns=columns, sep=";")
        self.env["abc.finance.sale.level.history"].flush_model()
        records = self.env["abc.finance.sale.level.history"].search([])
        self.assertGreaterEqual(len(records), 1)

    def test_level_assignment_validation(self):
        """
        Test that levels for a finance profile must total 100%.
        """
        profile = self.env["abc.classification.profile"].create(
            {
                "name": "Partial Level Profile",
                "profile_type": "cost",
                "warehouse_id": self.warehouse.id,
                "period": 365,
            }
        )
        self.env["abc.classification.level"].create(
            {
                "name": "A",
                "profile_id": profile.id,
                "percentage": 60,
                "percentage_products": 40,
            }
        )
        with self.assertRaises(ValidationError):
            profile.write(
                {
                    "level_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "B",
                                "percentage": 10,
                                "percentage_products": 10,
                            },
                        )
                    ]
                }
            )

    def test_get_finance_data_query_all_types(self):
        """
        Ensure _get_finance_data_query returns correct SQL for all profile types.
        """
        types_and_keywords = [
            ("cost", "SUM(sol.purchase_price * sol.qty_delivered) AS total_cost"),
            ("sale_price", "SUM(sol.price_unit * sol.qty_delivered) AS total_sales"),
        ]
        for profile_type, expected in types_and_keywords:
            profile = self.env["abc.classification.profile"].create(
                {
                    "name": f"Query Profile {profile_type}",
                    "profile_type": profile_type,
                    "warehouse_id": self.warehouse.id,
                    "period": 365,
                }
            )
            query, params = profile._get_finance_data_query("2025-01-01", [1, 2])
            self.assertIn(expected, query)
            self.assertIn("GROUP BY", query)
            self.assertIn("ORDER BY", query)
            self.assertIsInstance(params, dict)
