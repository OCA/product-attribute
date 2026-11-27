# Copyright (C) 2026 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductExpiryMonth(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create a product template with expiration enabled
        self.product_template = self.env["product.template"].create(
            {
                "name": "Test Product",
                "use_expiration_date": True,
                "tracking": "lot",
            }
        )

    def test_expiration_time_months_calculation(self):
        """Test that months are correctly converted to days"""
        # Test whole months - set months and check days
        self.product_template.expiration_time_months = 24
        self.assertEqual(self.product_template.expiration_time, 730)

        # Test fractional months
        self.product_template.expiration_time_months = 6.5
        self.assertEqual(self.product_template.expiration_time, 198)

        # Test zero months
        self.product_template.expiration_time_months = 0
        self.assertEqual(self.product_template.expiration_time, 0)

    def test_expiration_time_inverse_calculation(self):
        """Test that days are correctly converted to months"""
        # Test setting days and checking months
        self.product_template.expiration_time = 730
        self.assertEqual(round(self.product_template.expiration_time_months, 2), 24.0)

        # Test fractional days
        self.product_template.expiration_time = 198
        self.assertEqual(round(self.product_template.expiration_time_months, 2), 6.51)

        # Test zero days
        self.product_template.expiration_time = 0
        self.assertEqual(self.product_template.expiration_time_months, 0)

    def test_custom_days_per_year(self):
        """Test calculation with custom days per year"""
        # Change to leap year
        self.env["ir.config_parameter"].sudo().set_param(
            "product_expiry_month.days_per_year", "366"
        )

        self.product_template.expiration_time_months = 12
        # 366/12 = 30.5, so 12 months = 366 days
        self.assertEqual(self.product_template.expiration_time, 366)
