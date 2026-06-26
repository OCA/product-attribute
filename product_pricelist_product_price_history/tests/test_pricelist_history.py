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
        cls.variant_2 = cls.template_variants.product_variant_ids[1]

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

    def test_04_history_creation_specific_variant(self):
        """Updating a specific variant (not the first one) logs history correctly."""
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.variant_2.id,
                "fixed_price": 20.0,
            }
        )
        item.write({"fixed_price": 25.0})

        # The history record should be strictly attached to variant_2
        history_v2 = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.variant_2.id)]
        )
        self.assertEqual(len(history_v2), 1)
        self.assertEqual(history_v2.old_price, 20.0)
        self.assertEqual(history_v2.new_price, 25.0)

        # Ensure the change did NOT incorrectly log against variant_1
        history_v1 = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.variant_1.id), ("new_price", "=", 25.0)]
        )
        self.assertEqual(len(history_v1), 0)

    def test_05_no_history_on_other_field_update(self):
        """Updating fields other than fixed_price does not trigger a history log."""
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.product_simple.id,
                "fixed_price": 40.0,
                "min_quantity": 1,
            }
        )

        # Clear any history created by the initial create/setup if any
        self.env["product.pricelist.item.history"].search([]).unlink()

        # Update a non-price field
        item.write({"min_quantity": 10})

        history = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.product_simple.id)]
        )
        self.assertEqual(
            len(history), 0, "Updating min_quantity should not create a history record."
        )

    def test_06_batch_price_update(self):
        """Updating multiple pricelist items at once generates history for all"""
        item1 = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.variant_1.id,
                "fixed_price": 10.0,
            }
        )
        item2 = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_id": self.variant_2.id,
                "fixed_price": 20.0,
            }
        )

        # Perform a batch write
        items = item1 | item2
        items.write({"fixed_price": 50.0})

        # Verify history for item1
        history1 = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.variant_1.id)]
        )
        self.assertEqual(len(history1), 1)
        self.assertEqual(history1.new_price, 50.0)

        # Verify history for item2
        history2 = self.env["product.pricelist.item.history"].search(
            [("product_id", "=", self.variant_2.id)]
        )
        self.assertEqual(len(history2), 1)
        self.assertEqual(history2.new_price, 50.0)
