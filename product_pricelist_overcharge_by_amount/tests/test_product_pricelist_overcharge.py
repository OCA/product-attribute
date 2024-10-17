# Copyright 2024 Binhex - Christian Ramos
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestPricelistOvercharge(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product Test", "standard_price": 15, "list_price": 35}
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Overcharge Pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "price_round": 0.01,
                            "fixed_price": 30,
                            "price_discount": 0,
                            "overcharge": True,
                            "overcharge_item_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "applied_on": "equal",
                                        "min_price": 30,
                                        "overcharge_discount": -10,
                                        "overcharge_surcharge": 10,
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "applied_on": "smaller",
                                        "max_price": 70,
                                        "overcharge_discount": -20,
                                        "overcharge_surcharge": 20,
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "applied_on": "bigger",
                                        "min_price": 80,
                                        "overcharge_discount": -30,
                                        "overcharge_surcharge": 30,
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "applied_on": "between",
                                        "min_price": 100,
                                        "max_price": 120,
                                        "overcharge_discount": -40,
                                        "overcharge_surcharge": 40,
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "applied_on": "allways",
                                        "overcharge_discount": -50,
                                        "overcharge_surcharge": 50,
                                    },
                                ),
                            ],
                        },
                    ),
                ],
            }
        )

    def test_pricelist_overcharge(self):
        # equal
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            43,
        )
        self.pricelist.item_ids[0].write(
            {
                "fixed_price": 60,
            }
        )
        # smaller
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            92.0,
        )
        self.pricelist.item_ids[0].write(
            {
                "fixed_price": 90,
            }
        )
        # bigger
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            147.0,
        )
        self.pricelist.item_ids[0].write(
            {
                "fixed_price": 110,
            }
        )
        # between
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            173.0,
        )
        self.pricelist.item_ids[0].write(
            {
                "fixed_price": 75,
            }
        )
        # allways
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            162.5,
        )

    def test_pricelist_overcharge_constraint(self):
        with self.assertRaises(ValidationError) as ve:
            self.env["product.pricelist"].create(
                {
                    "name": "Overcharge Pricelist",
                    "item_ids": [
                        (
                            0,
                            0,
                            {
                                "compute_price": "fixed",
                                "fixed_price": 30,
                                "price_discount": 0,
                                "overcharge": True,
                                "overcharge_item_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "applied_on": "between",
                                            "min_price": 100,
                                            "max_price": 70,
                                            "overcharge_discount": -40,
                                            "overcharge_surcharge": 40,
                                        },
                                    ),
                                ],
                            },
                        ),
                    ],
                }
            )
        self.assertIn(
            "The minimum price should be lower than the maximum price.",
            ve.exception.args[0],
        )
