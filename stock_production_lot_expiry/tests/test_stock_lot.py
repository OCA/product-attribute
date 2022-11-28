# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestStockLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockLot, cls).setUpClass()
        cls.ProductProduct = cls.env["product.product"]
        cls.StockLot = cls.env["stock.lot"]
        cls.categ_lvl = cls.env.ref("product.product_category_all")
        cls.product = cls.ProductProduct.create(
            {
                "name": "test product",
                "specific_lot_expiry_field_name": "expiration_date",
            }
        )
        cls.today = datetime.now()
        cls.tomorrow = datetime.now() + timedelta(days=1)
        cls.yesterday = datetime.now() - timedelta(days=1)

    def test_00(self):
        """
        Data:
            * A product with value for specific_lot_expiry_field_name set to
              "expiration_date"
        Test case:
            1. Create a lot with a remove_date set to today
            2. Update the expiration_date on the lot to tomorrow
        Expected result:
            1. expiry_date on lot must be today
            2. expiry_date on lot must be tomorrow
        """
        self.assertEqual(self.product.lot_expiry_field_name, "expiration_date")

        lot = self.StockLot.create(
            {
                "name": "lot1",
                "product_id": self.product.id,
                "expiration_date": self.today,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertEqual(self.today, lot.expiry_date)
        lot.expiration_date = self.tomorrow
        self.assertEqual(self.tomorrow, lot.expiration_date)

    def test_01(self):
        """
        Data:
            * A product with value for specific_lot_expiry_field_name set to
              "removal_date"
        Test case:
            1. Create a lot with a remove_date set to today
            2. Update the removal_date on the lot to tomorrow
            3. Create a lot with a removal_date set to today
            4. Set the specific_lot_expiry_field_name on the product to
               'expiration_date'
            5. Update the expiration_date on the first lot to today
        Expected result:
            1. expiry_date is not set
            2. expiry_date is not tomorrow
            3. expiry_date on the new lot is set to today
            4. existing lot are not modified as long as a new value is not put
               into the specified field
            5. The expiry date on the first lot is st to today
        """
        self.product.specific_lot_expiry_field_name = "removal_date"
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")
        # 1
        lot = self.StockLot.create(
            {
                "name": "lot1",
                "product_id": self.product.id,
                "expiration_date": self.today,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertFalse(lot.expiry_date)

        # 2
        lot.removal_date = self.tomorrow
        self.assertEqual(self.tomorrow, lot.expiry_date)

        # 3
        new_lot = self.StockLot.create(
            {
                "name": "lot2",
                "product_id": self.product.id,
                "removal_date": self.today,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertEqual(self.today, new_lot.expiry_date)

        # 4
        self.product.specific_lot_expiry_field_name = "expiration_date"
        self.assertEqual(self.tomorrow, lot.expiry_date)
        lot.removal_date = False
        # since we assign a value to one of the field that can be used as
        # expiry field, the expiry_field is recomputed even if the modified
        # field is not the one updated
        self.assertEqual(self.today, lot.expiry_date)

        # 5
        lot.expiration_date = self.today
        self.assertEqual(self.today, lot.expiry_date)

    def test_02(self):
        """
         Data:
            * A product with value for specific_lot_expiry_field_name set to
              "removal_date"
        Test Case:
            1. Create a lot with a removal_date set to today
            2. Update the lot with a removal_date set to yesterday
        Expected result:
            1. The lot is not expired
            2. The lot is expired
        """
        self.product.specific_lot_expiry_field_name = "removal_date"
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")
        lot = self.StockLot.create(
            {
                "name": "lot1",
                "product_id": self.product.id,
                "removal_date": self.tomorrow,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertFalse(lot.product_expiry_alert)
        lot.removal_date = self.yesterday
        self.assertTrue(lot.product_expiry_alert)

    def test_03(self):
        """
        Data:
            An expired lot
        Test case:
            Search with different domain on the product_expiry_alert field
        """
        self.product.specific_lot_expiry_field_name = "removal_date"
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")
        lot = self.StockLot.create(
            {
                "name": "lot1",
                "product_id": self.product.id,
                "removal_date": self.yesterday,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertEqual(
            lot,
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "=", True),
                ]
            ),
        )
        self.assertEqual(
            lot,
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "!=", False),
                ]
            ),
        )
        self.assertFalse(
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "!=", True),
                ]
            )
        )
        self.assertFalse(
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "=", False),
                ]
            )
        )

    def test_04(self):
        """
        Data:
            One expired lot
            One not expired lot
            One lot that doesn't expire (no expiration date)
        Test case:
            1. Search for expired
            2. Search for not expired
        Expected result:
            1. Expired lot only must be returned
            2. Lot without expiration date and non expired lot must be returned
        """
        self.product.specific_lot_expiry_field_name = "removal_date"
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")
        expired_lot = self.StockLot.create(
            {
                "name": "lot expired",
                "product_id": self.product.id,
                "removal_date": self.yesterday,
                "company_id": self.env.user.company_id.id,
            }
        )
        not_expired_lot = self.StockLot.create(
            {
                "name": "lot not expired",
                "product_id": self.product.id,
                "removal_date": self.tomorrow,
                "company_id": self.env.user.company_id.id,
            }
        )
        no_expiring_lot = self.StockLot.create(
            {
                "name": "not expiring lot",
                "product_id": self.product.id,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.assertEqual(
            expired_lot,
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "=", True),
                ]
            ),
        )

        self.assertEqual(
            not_expired_lot | no_expiring_lot,
            self.StockLot.search(
                [
                    ("product_id", "=", self.product.id),
                    ("product_expiry_alert", "=", False),
                ]
            ),
        )
