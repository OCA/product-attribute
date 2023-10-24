# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProductPricelistFixedCurrencyRate(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist_model = cls.env["product.pricelist"]
        cls.product_model = cls.env["product.product"]

        cls.company = cls.env["res.company"].create(
            {
                "name": "Test",
                "currency_id": cls.env.ref("base.EUR").id,
            }
        )
        cls.env.user.company_id = cls.company

        cls.product_1 = cls.product_model.create(
            {
                "name": "Product 1",
                "list_price": 150.00,
                "company_id": cls.company.id,
            }
        )
        cls.product_2 = cls.product_model.create(
            {
                "name": "Product 1",
                "list_price": 200.00,
                "company_id": cls.company.id,
            }
        )

        cls.pricelist_eur = cls.pricelist_model.create(
            {
                "name": "Pricelist EUR",
                "currency_id": cls.env.ref("base.EUR").id,
                "company_id": cls.company.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "compute_price": "fixed",
                            "product_id": cls.product_1.id,
                            "fixed_price": 140.00,
                        },
                    )
                ],
            }
        )
        cls.pricelist_usd = cls.pricelist_model.create(
            {
                "name": "Pricelist USD",
                "currency_id": cls.env.ref("base.USD").id,
                "company_id": cls.company.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.pricelist_eur.id,
                        },
                    )
                ],
            }
        )
        cls.pricelist_usd_fixed_rate = cls.pricelist_model.create(
            {
                "name": "Pricelist USD",
                "currency_id": cls.env.ref("base.USD").id,
                "company_id": cls.company.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.pricelist_eur.id,
                            "fixed_currency_rate": 2.0,
                        },
                    )
                ],
            }
        )
        # Clean rates:
        cls.env["res.currency.rate"].search(
            [
                ("currency_id", "=", cls.env.ref("base.USD").id),
                ("company_id", "=", cls.company.id),
            ]
        ).unlink()
        cls.env["res.currency.rate"].create(
            {
                "name": "2023-01-01",
                "rate": 1.5,
                "currency_id": cls.env.ref("base.USD").id,
                "company_id": cls.company.id,
            }
        )

    def test_01_pricelist_currency_rate(self):
        # Product 1 (item in base pricelist)
        self.assertEqual(self.env.company.currency_id, self.env.ref("base.EUR"))
        eur_price_1 = self.pricelist_eur._get_product_price(self.product_1, 1.0)
        self.assertEqual(eur_price_1, 140.0)
        usd_price_1 = self.pricelist_usd._get_product_price(self.product_1, 1.0)
        expected = 140 * 1.5
        self.assertEqual(usd_price_1, expected)
        usd_fr_price_1 = self.pricelist_usd_fixed_rate._get_product_price(
            self.product_1, 1.0
        )
        expected = 140 * 2.0
        self.assertEqual(usd_fr_price_1, expected)
        # Product 2 (no item in base pricelist)
        eur_price_2 = self.pricelist_eur._get_product_price(self.product_2, 1.0)
        self.assertEqual(eur_price_2, 200.0)
        usd_price_2 = self.pricelist_usd._get_product_price(self.product_2, 1.0)
        expected = 200 * 1.5
        self.assertEqual(usd_price_2, expected)
        usd_fr_price_2 = self.pricelist_usd_fixed_rate._get_product_price(
            self.product_2, 1.0
        )
        expected = 200 * 2.0
        self.assertEqual(usd_fr_price_2, expected)

    def test_02_auxiliary_fields(self):
        item = self.pricelist_usd_fixed_rate.item_ids
        self.assertTrue(item.is_fixed_currency_rate_applicable)
        self.assertEqual(item.actual_currency_rate, 1.5)
