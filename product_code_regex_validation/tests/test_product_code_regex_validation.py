# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductCodeRegExValidation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.product_categ_obj = cls.env["product.category"]
        cls.category = cls.product_categ_obj.create(
            {"name": "Test Category", "product_code_regex_validation": "A[0-9]"}
        )
        cls.product = cls.product_obj.create(
            {"name": "Test Product", "categ_id": cls.category.id, "default_code": False}
        )

    def test_01_modify_default_code(self):
        """Error triggered when modifying the default code not following the format"""
        with self.assertRaises(ValidationError):
            self.product.default_code = "B1"

    def test_02_create_new_product(self):
        """Error triggered when creating new product not following the format"""
        with self.assertRaises(ValidationError):
            self.product_obj.create(
                {
                    "name": "Test Product 2",
                    "categ_id": self.category.id,
                    "default_code": "B1",
                }
            )

    def test_03_modify_regex(self):
        """Error triggered when modifying the regex format and some product does
        not follow it."""
        self.product.default_code = "A1"
        with self.assertRaises(ValidationError):
            self.category.product_code_regex_validation = "B[0-9]"

    def test_04_ignore_archived_product(self):
        """Archived product is ignored and no error is triggered when modifying the
        regex format"""
        self.product.default_code = "A1"
        self.product.active = False
        self.category.product_code_regex_validation = "B[0-9]"
        # Error triggered when unarchiving
        with self.assertRaises(ValidationError):
            self.product.active = True

    def test_05_modify_product_category(self):
        """Error triggered when modifying the category and format is not valid"""
        self.category_2 = self.product_categ_obj.create(
            {"name": "Test Category 2", "product_code_regex_validation": "B[0-9]"}
        )
        self.product.default_code = "A1"
        with self.assertRaises(ValidationError):
            self.product.categ_id = self.category_2
