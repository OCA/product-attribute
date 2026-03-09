# Copyright 2026 Tecnativa - Andrii Kompaniiets
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged
from odoo.tools.misc import mute_logger


@tagged("post_install", "-at_install")
class TestDiscountRange(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
            }
        )
        cls.pricelist_item = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist.id,
                "compute_price": "formula",
                "base": "standard_price",
                "discount_type": "range",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )

    def test_create_valid_range(self):
        range1 = self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 0.01,
                "max": 100,
                "percentage": 10,
            }
        )
        self.assertEqual(range1.min, 0.01)
        self.assertEqual(range1.max, 100)

    @mute_logger("odoo.sql_db")
    def test_invalid_min_gt_max(self):
        with self.assertRaises(IntegrityError):
            self.env["product.pricelist.item.discount_range"].create(
                {
                    "pricelist_item_id": self.pricelist_item.id,
                    "min": 200,
                    "max": 100,
                    "percentage": 10,
                }
            )
            self.env["product.pricelist.item.discount_range"].flush()

    def test_overlap_range(self):
        self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 0.01,
                "max": 100,
                "percentage": 10,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["product.pricelist.item.discount_range"].create(
                {
                    "pricelist_item_id": self.pricelist_item.id,
                    "min": 50,
                    "max": 150,
                    "percentage": 15,
                }
            )

    def _calculate_price(self):
        product_price = self.pricelist._compute_price_rule(self.product, 1.0)
        return product_price[self.product.id][0]

    def test_discount_application_for_standard_price(self):
        self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 0.01,
                "max": 24.99,
                "percentage": -10,
            }
        )
        self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 25,
                "max": 50,
                "percentage": -20,
            }
        )
        self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 70.01,
                "max": 100,
                "percentage": -50,
            }
        )
        self.product.standard_price = 10.0
        self.assertEqual(
            self._calculate_price(), 11.0, "Price should be 10% up for price 10"
        )
        self.product.standard_price = 55.0
        with self.assertRaises(ValidationError):
            self._calculate_price()  # no range for this cost
        self.product.standard_price = 70.02
        self.assertEqual(
            self._calculate_price(), 105.03, "Price should be 50% up for price 70.02"
        )

    def test_discount_application_for_list_price(self):
        self.pricelist_item.base = "list_price"
        self.env["product.pricelist.item.discount_range"].create(
            {
                "pricelist_item_id": self.pricelist_item.id,
                "min": 0.01,
                "max": 100,
                "percentage": -10,
            }
        )
        self.product.list_price = 20.0
        self.assertEqual(
            self._calculate_price(), 22.0, "Price should be 10% up for price 20"
        )
