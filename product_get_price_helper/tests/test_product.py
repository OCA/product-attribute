# Copyright 2017 Akretion (http://www.akretion.com).
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class ProductCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env.ref("product.product_product_4_product_template")
        cls.variant = cls.env.ref("product.product_product_4b")
        cls.template.taxes_id = cls.env.ref("product_get_price_helper.tax_1")
        cls.env.user.company_id.currency_id = cls.env.ref("base.USD")
        cls.base_pricelist = cls.env.ref("product.list0")
        cls.base_pricelist.currency_id = cls.env.ref("base.USD")
        cls.variant.currency_id = cls.env.ref("base.USD")

    def test_product_simple_get_price(self):
        self.assertEqual(
            self.variant._get_price(),
            {
                "discount": 0.0,
                "original_value": 750.0,
                "tax_included": True,
                "value": 750.0,
            },
        )

    def test_product_price_rounding(self):
        # Odony example: https://gist.github.com/odony/5269a695545902e7e23e761e20a9ec8c
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.base_pricelist.id,
                "product_id": self.variant.id,
                "base": "list_price",
                "applied_on": "0_product_variant",
                "compute_price": "percentage",
                "percent_price": 50,
            }
        )
        self.variant.list_price = 423.4
        self.assertEqual(
            self.variant._get_price(pricelist=self.base_pricelist)["value"], 211.70
        )

    def test_product_get_price(self):
        # self.base_pricelist doesn't define a tax mapping. We are tax included
        fiscal_position_fr = self.env.ref("product_get_price_helper.fiscal_position_0")
        price = self.variant._get_price(
            pricelist=self.base_pricelist, fposition=fiscal_position_fr
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 750.0,
                "tax_included": True,
                "value": 750.0,
            },
        )
        # promotion price list define a discount of 20% on all product
        promotion_price_list = self.env.ref("product_get_price_helper.pricelist_1")
        price = self.variant._get_price(
            pricelist=promotion_price_list, fposition=fiscal_position_fr
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 600.0,
                "tax_included": True,
                "value": 600.0,
            },
        )
        # use a fiscal position defining a mapping from tax included to tax
        # excluded
        tax_exclude_fiscal_position = self.env.ref(
            "product_get_price_helper.fiscal_position_1"
        )
        price = self.variant._get_price(
            pricelist=self.base_pricelist, fposition=tax_exclude_fiscal_position
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 652.17,
                "tax_included": False,
                "value": 652.17,
            },
        )
        price = self.variant._get_price(
            pricelist=promotion_price_list, fposition=tax_exclude_fiscal_position
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 521.74,
                "tax_included": False,
                "value": 521.74,
            },
        )

    def test_product_get_price_zero(self):
        # Test that discount calculation does not fail if original price is 0
        self.variant.list_price = 0
        self.base_pricelist.discount_policy = "without_discount"
        self.env["product.pricelist.item"].create(
            {
                "product_id": self.variant.id,
                "pricelist_id": self.base_pricelist.id,
                "fixed_price": 10,
            }
        )
        fiscal_position_fr = self.env.ref("product_get_price_helper.fiscal_position_0")
        price = self.variant._get_price(
            pricelist=self.base_pricelist, fposition=fiscal_position_fr
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 0.0,
                "tax_included": True,
                "value": 10.0,
            },
        )

    def test_product_get_price_per_qty(self):
        # Define a promotion price for the product with min_qty = 10
        fposition = self.env.ref("product_get_price_helper.fiscal_position_0")
        pricelist = self.base_pricelist
        self.env["product.pricelist.item"].create(
            {
                "name": "Discount on Product when Qty >= 10",
                "pricelist_id": pricelist.id,
                "base": "list_price",
                "compute_price": "percentage",
                "percent_price": "20",
                "applied_on": "0_product_variant",
                "product_id": self.variant.id,
                "min_quantity": 10.0,
            }
        )
        # Case 1 (qty = 1.0). No discount is applied
        price = self.variant._get_price(
            qty=1.0, pricelist=pricelist, fposition=fposition
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 750.0,
                "tax_included": True,
                "value": 750.0,
            },
        )
        # Case 2 (qty = 10.0). Discount is applied
        # promotion price list define a discount of 20% on all product
        price = self.variant._get_price(
            qty=10.0, pricelist=pricelist, fposition=fposition
        )
        self.assertDictEqual(
            price,
            {
                "discount": 0.0,
                "original_value": 600.0,
                "tax_included": True,
                "value": 600.0,
            },
        )

    def test_product_get_price_discount_policy(self):
        # Ensure that discount is with 2 digits
        self.env.ref("product.decimal_discount").digits = 2
        # self.base_pricelist doesn't define a tax mapping. We are tax included
        # we modify the discount_policy
        self.base_pricelist.discount_policy = "without_discount"
        fiscal_position_fr = self.env.ref("product_get_price_helper.fiscal_position_0")
        price = self.variant._get_price(
            pricelist=self.base_pricelist, fposition=fiscal_position_fr
        )
        self.assertDictEqual(
            price,
            {
                "tax_included": True,
                "value": 750.0,
                "discount": 0.0,
                "original_value": 750.0,
            },
        )
        # promotion price list define a discount of 20% on all product
        # we modify the discount_policy
        promotion_price_list = self.env.ref("product_get_price_helper.pricelist_1")
        promotion_price_list.discount_policy = "without_discount"
        price = self.variant._get_price(
            pricelist=promotion_price_list, fposition=fiscal_position_fr
        )
        self.assertDictEqual(
            price,
            {
                "tax_included": True,
                "value": 600.0,
                "discount": 20.0,
                "original_value": 750.0,
            },
        )
        # use the fiscal position defining a mapping from tax included to tax
        # excluded
        # Tax mapping should not impact the computation of the discount and
        # the original value
        tax_exclude_fiscal_position = self.env.ref(
            "product_get_price_helper.fiscal_position_1"
        )
        price = self.variant._get_price(
            pricelist=self.base_pricelist, fposition=tax_exclude_fiscal_position
        )
        self.assertDictEqual(
            price,
            {
                "tax_included": False,
                "value": 652.17,
                "discount": 0.0,
                "original_value": 652.17,
            },
        )
        price = self.variant._get_price(
            pricelist=promotion_price_list, fposition=tax_exclude_fiscal_position
        )
        self.assertDictEqual(
            price,
            {
                "tax_included": False,
                "value": 521.74,
                "discount": 20.0,
                "original_value": 652.17,
            },
        )
