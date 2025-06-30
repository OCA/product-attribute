# Copyright 2018 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductRestrictedType(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product_product = self.env["product.product"]
        self.product_category = self.env["product.category"]

        self.product_types = self.env["product.template"]._fields["type"].selection

        self.categ_test = self.product_category.create(
            {
                "name": "Test Category 1",
                "restricted_product_type": self.product_types[0][0],
            }
        )
        self.categ_test2 = self.product_category.create({"name": "Test Category 2"})
        self.product_test = self.product_product.create(
            {
                "name": "Test Product 1",
                "type": self.product_types[0][0],
                "categ_id": self.categ_test.id,
            }
        )
        self.product_product.create(
            {
                "name": "Test Product 2",
                "type": self.product_types[1][0],
                "categ_id": self.categ_test2.id,
            }
        )

    def test_01_product_different_type(self):
        """User tries to change product type to a different type than
        company restricted product type"""
        with self.assertRaises(ValidationError):
            self.product_test.write({"type": self.product_types[1][0]})
        with self.assertRaises(ValidationError):
            self.product_product.create(
                {
                    "name": "Test Product 3",
                    "type": self.product_types[1][0],
                    "categ_id": self.categ_test.id,
                }
            )

    def test_02_category_different_type(self):
        """User tries to change category restricted type but there are
        products with already defined (different) type"""
        with self.assertRaises(ValidationError):
            self.categ_test.write({"restricted_product_type": self.product_types[1][0]})

    def test_03_type_equals_restricted_type(self):
        """
        Ensure the product template's type is updated to match the category's
        restricted product type.
        """
        product_template_test = self.env["product.template"].create(
            {
                "name": "Test Product Template",
                "type": self.product_types[0][0],
                "categ_id": self.categ_test.id,
            }
        )

        self.assertEqual(
            product_template_test.type,
            self.categ_test.restricted_product_type,
            "The product template's type should have been updated to the "
            "restricted product type of the category.",
        )

    def test_04_domain_changes_with_type(self):
        """
        Check that only allowed categories can be selected based
        on the product type
        """

        categ_consummable = self.product_category.create(
            {
                "name": "Test Category 1",
                "restricted_product_type": self.product_types[0][0],
            }
        )
        categ_service = self.product_category.create(
            {
                "name": "Test Category 1",
                "restricted_product_type": self.product_types[1][0],
            }
        )
        categ_no_restriction = self.product_category.create(
            {"name": "General Category", "restricted_product_type": False}
        )

        product_template_test2 = self.env["product.template"].create(
            {
                "name": "Test Product Template 1",
                "type": self.product_types[1][0],
                "categ_id": categ_service.id,
            }
        )

        self.assertIn(
            categ_service,
            product_template_test2.allowed_categ_ids,
            "Service category should be included for service type",
        )
        self.assertNotIn(
            categ_consummable,
            product_template_test2.allowed_categ_ids,
            "Consummable category should not be included for service type",
        )
        self.assertIn(
            categ_no_restriction,
            product_template_test2.allowed_categ_ids,
            "General category should always be included",
        )
