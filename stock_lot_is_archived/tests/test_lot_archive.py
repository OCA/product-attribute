# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestStockLotArchive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.lot_obj = cls.env["stock.lot"]
        cls.archive_wizard_obj = cls.env["stock.lot.archive"]
        cls.product = cls.product_obj.create({"name": "Product 1", "tracking": "lot"})
        cls.lot = cls.lot_obj.create(
            {
                "product_id": cls.product.id,
                "name": "TEST",
                "expiration_date": "2022-06-01",
                "company_id": cls.env.company.id,
            }
        )

        cls.newer_lot = cls.lot_obj.create(
            {
                "product_id": cls.product.id,
                "name": "TEST 2",
                "expiration_date": "2022-07-01",
                "company_id": cls.env.company.id,
            }
        )

    def test_lot_archive(self):
        """
        Check that the archiving method is archiving the
        elder lot
        """
        self.assertFalse(self.lot.is_archived)
        self.assertFalse(self.newer_lot.is_archived)
        self.archive_wizard_obj._archive_lots()
        self.assertTrue(self.lot.is_archived)
        self.assertFalse(self.newer_lot.is_archived)

    def test_lot_archive_editable(self):
        """
        With a user which is not stock manager check the editable is False
        Then add the the stock manager group, editable should be True
        """
        user_demo = self.env.ref("base.user_demo")
        lot_demo = self.lot.with_user(user_demo)
        user_demo.groups_id -= self.env.ref("stock.group_stock_manager")
        self.assertFalse(lot_demo.is_archived_editable)
        user_demo.groups_id += self.env.ref("stock.group_stock_manager")
        lot_demo = self.lot.with_user(user_demo)
        self.assertTrue(lot_demo.is_archived_editable)
