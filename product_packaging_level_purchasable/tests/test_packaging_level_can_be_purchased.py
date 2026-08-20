# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.exceptions import ValidationError

from .common import Common


class TestPackagingLevelCanBePurchased(Common):
    @classmethod
    def setUpClassPurchaseOrder(cls):
        super().setUpClassPurchaseOrder()
        cls.order_line.product_uom_qty = 3.0
        # Needed for W8110 of pylint-odoo.
        return None

    def test_packaging_level_can_be_purchased(self):
        self.order_line.write({"product_packaging_id": self.packaging_tu.id})
        with self.assertRaises(ValidationError):
            self.order_line.write(
                {"product_packaging_id": self.packaging_cannot_be_purchased.id}
            )
            onchange_res = self.order_line._onchange_product_packaging_id()
            self.assertIn("warning", onchange_res)

    def test_product_packaging_can_be_purchased(self):
        """Check that a product.packaging can be
        independently set as can be purchased."""
        exception_msg = (
            "Packaging Test packaging cannot be purchased on product {} must be set "
            "as 'Can be purchased' in order to be used on a purchase order."
        ).format(self.product.name)
        with self.assertRaisesRegex(ValidationError, exception_msg):
            self.order_line.write(
                {"product_packaging_id": self.packaging_cannot_be_purchased.id}
            )
        # Packaging can be purchased even if the packaging level does not allows it
        self.packaging_cannot_be_purchased.can_be_purchased = True
        self.order_line.write(
            {"product_packaging_id": self.packaging_cannot_be_purchased.id}
        )
        # Changing the packaging level on product.packaging updates can_be_purchased
        self.purchasable_packagings.unlink()
        self.packaging_cannot_be_purchased.packaging_level_id = self.packaging_level_tu
        self.packaging_cannot_be_purchased.packaging_level_id = (
            self.packaging_level_cannot_be_purchased
        )
        self.assertEqual(self.packaging_cannot_be_purchased.can_be_purchased, False)
        # Changing the can_be_purchased on the packaging_level
        # does not update the packaging
        self.packaging_level_cannot_be_purchased.can_be_purchased = True
        self.assertEqual(self.packaging_cannot_be_purchased.can_be_purchased, False)

    def test_onchange_product_packaging_valid(self):
        """Test the onchange method with a valid packaging."""
        # Ensure packaging is valid for purchase
        self.packaging_tu.can_be_purchased = True
        self.order_line.product_packaging_id = self.packaging_tu.id
        # This should return a result from super() method,
        # but not the 'cannot be purchased' warning
        onchange_res = self.order_line._onchange_product_packaging_id()
        # Check that we got a warning (from super) but not our specific warning
        self.assertIn("warning", onchange_res)
        # Make sure it's not our specific warning about "Can be purchased"
        self.assertNotIn(
            "Can be purchased", onchange_res.get("warning", {}).get("message", "")
        )

    def test_compute_product_packaging_id(self):
        """Test that the compute method removes non-purchasable packaging."""
        # Create a new order line to avoid constraints during setup
        new_line = self.env["purchase.order.line"].new(
            {
                "order_id": self.order.id,
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
            }
        )

        # Test non-purchasable packaging
        self.packaging_cannot_be_purchased.can_be_purchased = False
        # Bypass the constraints by using new() and setting the attribute directly
        new_line.product_packaging_id = self.packaging_cannot_be_purchased

        # Force compute method
        new_line._compute_product_packaging_id()

        # Check that the packaging was removed
        self.assertFalse(new_line.product_packaging_id)

        # Now test with a purchasable packaging
        self.packaging_tu.can_be_purchased = True
        new_line.product_packaging_id = self.packaging_tu
        new_line._compute_product_packaging_id()

        # The purchasable packaging should remain
        self.assertEqual(new_line.product_packaging_id, self.packaging_tu)
