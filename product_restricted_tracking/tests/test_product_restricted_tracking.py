# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductRestrictedTracking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_serial = cls.env["product.category"].create(
            {"name": "Serial Category", "restricted_tracking": "serial"}
        )
        cls.category_lot = cls.env["product.category"].create(
            {"name": "Lot Category", "restricted_tracking": "lot"}
        )
        cls.category_unrestricted = cls.env["product.category"].create(
            {"name": "Unrestricted Category"}
        )
        cls.product_serial = cls.env["product.template"].create(
            {
                "name": "Serial Product",
                "tracking": "serial",
                "categ_id": cls.category_serial.id,
            }
        )

    def test_product_mismatch_category_tracking_fails(self):
        """Product with mismatched tracking raises validation error."""
        with self.assertRaises(ValidationError):
            self.env["product.template"].create(
                {
                    "name": "Lot Product",
                    "tracking": "lot",
                    "categ_id": self.category_serial.id,
                }
            )
        with self.assertRaises(ValidationError):
            self.product_serial.tracking = "lot"
        with self.assertRaises(ValidationError):
            self.product_serial.categ_id = self.category_lot

    def test_unrestricted_category_allows_any_tracking(self):
        """Unrestricted category accepts any tracking value."""
        product = self.env["product.template"].create(
            {
                "name": "Lot Product",
                "tracking": "lot",
                "categ_id": self.category_unrestricted.id,
            }
        )
        self.assertEqual(product.tracking, "lot")
        product.tracking = "serial"
        self.assertEqual(product.tracking, "serial")
        product.tracking = "none"
        self.assertEqual(product.tracking, "none")

    def test_category_restriction_change_with_conflicting_products_fails(self):
        with self.assertRaises(ValidationError):
            self.category_serial.restricted_tracking = "lot"

    def test_category_restriction_clear_succeeds(self):
        self.category_serial.restricted_tracking = False
        self.assertFalse(self.category_serial.restricted_tracking)
