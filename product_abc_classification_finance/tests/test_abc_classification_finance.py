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
            cls.warehouse = cls.env["stock.warehouse"].create({
                "name": "Test Warehouse",
                "code": "TST",
                "reception_steps": "one_step",
                "delivery_steps": "ship_only",
            })

        # Create ABC profile for finance (cost based)
        cls.finance_profile = cls.env["abc.classification.profile"].create({
            "name": "Test Finance Cost Profile",
            "profile_type": "cost",
            "warehouse_id": cls.warehouse.id,
            "period": 365,
        })

        # Create levels for the profile
        cls.level_A = cls.env["abc.classification.level"].create({
            "name": "A",
            "profile_id": cls.finance_profile.id,
            "percentage": 70,
            "percentage_products": 30,
        })
        cls.level_B = cls.env['abc.classification.level'].create({
            'name': 'B',
            'profile_id': cls.finance_profile.id,
            'percentage': 30,
            'percentage_products': 70,
        })
        
        # Create a product
        cls.product = cls.env["product.product"].create({
            "name": "Finance Product",
            "uom_id": cls.env.ref("uom.product_uom_unit").id,
            "type": "product",
            "default_code": "FIN001",
            "tracking": "none",
        })

    def test_profile_requires_warehouse(self):
        """
        Finance profile must require a warehouse.
        """
        profile = self.env["abc.classification.profile"].new({
            "name": "No Warehouse",
            "profile_type": "cost",
            "warehouse_id": False,
        })
        with self.assertRaises(ValidationError):
            profile._check_warehouse_id()

    def test_finance_profile_type_selection(self):
        """
        Profile type should accept 'cost', 'sale_price', 'sale_margin'.
        """
        for profile_type in ["cost", "sale_price", "sale_margin"]:
            profile = self.env["abc.classification.profile"].create({
                "name": f"Profile {profile_type}",
                "profile_type": profile_type,
                "warehouse_id": self.warehouse.id,
            })
            self.assertEqual(profile.profile_type, profile_type)

    def test_history_record_creation(self):
        """
        Test that finance history records can be created and linked to product level.
        """
        product_level = self.env["abc.classification.product.level"].create({
            "product_id": self.product.id,
            "computed_level_id": self.level_A.id,
            "profile_id": self.finance_profile.id,
        })
        history = self.env["abc.finance.sale.level.history"].create({
            "computed_level_id": self.level_A.id,
            "product_id": self.product.id,
            "purchase_price": 10.0,
            "margin": 2.0,
            "total_cost": 100.0,
            "total_sales": 120.0,
            "profile_id": self.finance_profile.id,
            "warehouse_id": self.warehouse.id,
            "product_level_id": product_level.id,
        })
        self.assertEqual(history.product_id, self.product)
        self.assertEqual(history.product_level_id, product_level)
        self.assertEqual(product_level.finance_sale_level_history_ids, history)

    def test_finance_data_query_methods(self):
        """
        Smoke test for _get_finance_data_query and _finance_init_collected_data_instance.
        """
        from_date = "2025-01-01"
        customer_location_ids = []
        query, params = self.finance_profile._get_finance_data_query(from_date, customer_location_ids)
        self.assertIsInstance(query, str)
        self.assertIsInstance(params, dict)
        self.assertIn("SUM(", query)
        self.assertIn("GROUP BY", query)
        self.assertIn("ORDER BY", query)
        data_instance = self.finance_profile._finance_init_collected_data_instance()
        self.assertEqual(data_instance.profile, self.finance_profile)

    def test_level_assignment_validation(self):
        """
        Test that levels for a finance profile must total 100%.
        """
        profile = self.env["abc.classification.profile"].create({
            "name": "Partial Level Profile",
            "profile_type": "cost",
            "warehouse_id": self.warehouse.id,
        })
        self.env["abc.classification.level"].create({
            "name": "A",
            "profile_id": profile.id,
            "percentage": 60,
            "percentage_products": 40,
        })
        with self.assertRaises(ValidationError):
            profile.write(
                {
                    "level_ids": [
                        (
                            0,
                            0,
                            {"name": "B", "percentage": 10, "percentage_products": 10},
                        )
                    ]
                }
            )
