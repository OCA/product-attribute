from datetime import date

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestProductIdCategory(TransactionCase):
    def test_create_id_category(self):
        """Test creation of product identification category"""
        category = self.env["product.product.id_category"].create(
            {"name": "Regulatory ID"}
        )
        self.assertTrue(category.id, "Product ID Category creation failed")
        self.assertEqual(
            category.name, "Regulatory ID", "Product ID Category name mismatch"
        )


class TestProductIdNumber(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Issuer"})
        self.product = self.env["product.product"].create({"name": "Test Product"})
        self.category = self.env["product.product.id_category"].create(
            {"name": "Batch Number"}
        )

    def test_create_id_number(self):
        """Test creation of product identification number"""
        id_number = self.env["product.product.id_number"].create(
            {
                "name": "ID123456",
                "category_id": self.category.id,
                "issued_by": self.partner.id,
                "date_issued": "2024-09-01",
                "expiry_date": "2025-09-01",
                "place_of_issue": "City A",
                "product_id": self.product.id,
            }
        )
        self.assertTrue(id_number.id, "Product ID Number creation failed")
        self.assertEqual(id_number.name, "ID123456", "Product ID Number mismatch")
        self.assertEqual(
            id_number.category_id.id,
            self.category.id,
            "Category not assigned correctly",
        )
        self.assertEqual(
            id_number.product_id.id, self.product.id, "Product not assigned correctly"
        )


class TestProductIdNumberCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Issuer"})
        self.product = self.env["product.product"].create({"name": "Test Product"})
        self.category = self.env["product.product.id_category"].create(
            {"name": "Batch Number"}
        )

    def test_create_id_number(self):
        """Test creation of product identification number"""
        id_number = self.env["product.product.id_number"].create(
            {
                "name": "ID123456",
                "category_id": self.category.id,
                "issued_by": self.partner.id,
                "date_issued": "2024-09-01",
                "expiry_date": "2025-09-01",
                "place_of_issue": "City A",
                "product_id": self.product.id,
            }
        )
        self.assertTrue(id_number.id, "Product ID Number creation failed")
        self.assertEqual(id_number.name, "ID123456", "Product ID Number mismatch")
        self.assertEqual(
            id_number.category_id.id,
            self.category.id,
            "Category not assigned correctly",
        )
        self.assertEqual(
            id_number.product_id.id, self.product.id, "Product not assigned correctly"
        )


class TestProductIdExpiryNotification(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "responsible_id": self.env["res.users"]
                .create(
                    {
                        "name": "Test Responsible",
                        "login": "test_responsible",
                        "email": "responsible@test.com",
                    }
                )
                .id,
            }
        )
        self.category = self.env["product.product.id_category"].create(
            {"name": "Regulatory ID"}
        )

    def test_cron_expiry_notification(self):
        """Test if the cron job sends expiry notification"""
        # Create an ID number that is expiring today
        self.env["product.product.id_number"].create(
            {
                "name": "ID123456",
                "category_id": self.category.id,
                "expiry_date": fields.Date.today(),
                "product_id": self.product.id,
            }
        )

        # Run the cron manually
        self.env[
            "product.product.id_number"
        ]._cron_send_product_regi_expiry_notification()

        # Check if a mail was created
        mail = self.env["mail.mail"].search(
            [("email_to", "=", self.product.responsible_id.email)], limit=1
        )
        self.assertTrue(mail, "No email was sent for expiring product identification")
        self.assertIn(
            "Product Registration Expiry Notification",
            mail.subject,
            "Email subject mismatch",
        )


class TestProductIdNumberDateValidation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.category = self.env["product.product.id_category"].create(
            {"name": "Regulatory ID"}
        )
        self.product = self.env["product.product"].create({"name": "Test Product"})

    def test_valid_dates(self):
        """Test valid date_issued and expiry_date"""
        id_number = self.env["product.product.id_number"].create(
            {
                "name": "ID123456",
                "category_id": self.category.id,
                "date_issued": date(2024, 9, 1),
                "expiry_date": date(2025, 9, 1),
                "product_id": self.product.id,
            }
        )
        self.assertTrue(
            id_number.id, "Product ID Number with valid dates should be created"
        )

    def test_invalid_dates(self):
        """Test invalid date_issued > expiry_date"""
        with self.assertRaises(
            ValidationError,
            msg="ValidationError should be raised for invalid date range",
        ):
            self.env["product.product.id_number"].create(
                {
                    "name": "ID123457",
                    "category_id": self.category.id,
                    "date_issued": date(2025, 9, 1),
                    "expiry_date": date(2024, 9, 1),
                    "product_id": self.product.id,
                }
            )
