# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo.addons.base.tests.common import BaseCommon


class TestProductExpiryAlert(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "tracking": "lot",
                "use_expiration_date": True,
            }
        )

        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "Test Lot",
                "product_id": cls.product.id,
                "expiration_date": "2025-01-31",
                "use_date": "2025-01-25",
                "removal_date": "2025-01-20",
                "alert_date": "2025-01-15",
            }
        )

    def test_removal_alert(self):
        # Check no date is expired
        with freeze_time("2025-01-14"):
            self.assertFalse(self.lot.product_alert_date_expiry_alert)
            self.assertFalse(self.lot.product_removal_date_expiry_alert)
            self.assertFalse(self.lot.product_use_date_expiry_alert)
        self.lot.invalidate_recordset()
        # Check only the alert date is expired
        with freeze_time("2025-01-16"):
            self.assertTrue(self.lot.product_alert_date_expiry_alert)
            self.assertFalse(self.lot.product_removal_date_expiry_alert)
            self.assertFalse(self.lot.product_use_date_expiry_alert)
        self.lot.invalidate_recordset()
        # Check alert and removal date are expired
        with freeze_time("2025-01-21"):
            self.assertTrue(self.lot.product_alert_date_expiry_alert)
            self.assertTrue(self.lot.product_removal_date_expiry_alert)
            self.assertFalse(self.lot.product_use_date_expiry_alert)
        self.lot.invalidate_recordset()
        # Check all date (except expiration) are expired
        with freeze_time("2025-01-26"):
            self.assertTrue(self.lot.product_alert_date_expiry_alert)
            self.assertTrue(self.lot.product_removal_date_expiry_alert)
            self.assertTrue(self.lot.product_use_date_expiry_alert)

    def test_removal_alert_search(self):
        # Check no date is expired
        with freeze_time("2025-01-14"):
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_alert_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_removal_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_use_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)

            # True values
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_alert_date_expiry_alert", "=", True),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_removal_date_expiry_alert", "=", True),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_use_date_expiry_alert", "=", True),
                ]
            )
            self.assertFalse(lot)

        with freeze_time("2025-01-16"):
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_alert_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_removal_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_use_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)

        with freeze_time("2025-01-21"):
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_alert_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_removal_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_use_date_expiry_alert", "=", False),
                ]
            )
            self.assertTrue(lot)

        with freeze_time("2025-01-26"):
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_alert_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_removal_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
            lot = self.env["stock.lot"].search(
                [
                    ("product_id", "=", self.lot.product_id.id),
                    ("product_use_date_expiry_alert", "=", False),
                ]
            )
            self.assertFalse(lot)
