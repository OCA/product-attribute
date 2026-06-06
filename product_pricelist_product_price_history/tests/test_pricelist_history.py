# Copyright 2026 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPricelistHistorySimple(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "General Pricelist"}
        )
        cls.product_simple = cls.env["product.product"].create(
            {"name": "Simple Product", "lst_price": 10.0}
        )
        cls.template_variants = cls.env["product.template"].create(
            {
                "name": "Configurable Product",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.env.ref(
                                "product.product_attribute_1"
                            ).id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        cls.env.ref(
                                            "product.product_attribute_value_1"
                                        ).id,
                                        cls.env.ref(
                                            "product.product_attribute_value_2"
                                        ).id,
                                    ],
                                )
                            ],
                        },
                    )
                ],
            }
        )
        cls.variant_1 = cls.template_variants.product_variant_ids[0]

    def test_01_history_creation_variant_direct(self):
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.product_simple.id,
                "fixed_price": 50.0,
            }
        )
        item.write({"fixed_price": 60.0})

        history = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.product_simple.id)]
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history.old_price, 50.0)
        self.assertEqual(history.new_price, 60.0)

    def test_02_history_creation_template(self):
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_tmpl_id": self.template_variants.id,
                "fixed_price": 100.0,
            }
        )
        item.write({"fixed_price": 120.0})

        history = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.variant_1.id)]
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history.old_price, 100.0)
        self.assertEqual(history.new_price, 120.0)

    def test_03_no_history_on_same_price(self):
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.product_simple.id,
                "fixed_price": 50.0,
            }
        )
        item.write({"fixed_price": 50.0})

        history = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.product_simple.id)]
        )
        self.assertEqual(len(history), 0)
