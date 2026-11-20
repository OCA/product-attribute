# Copyright 2017 Akretion (http://www.akretion.com).
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# Copyright 2025 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.tests import TransactionCase


class ProductCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.country_id = cls.env.ref("base.us")
        cls.tax_group = cls.env["account.tax.group"].create(
            {
                "name": "Test Tax Group",
            }
        )
        cls.tax_1 = cls.env["account.tax"].create(
            {
                "name": "Tax inc demo",
                "amount": 15.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include": True,
                "tax_group_id": cls.tax_group.id,
            }
        )
        cls.tax_2 = cls.env["account.tax"].create(
            {
                "name": "Tax exc demo",
                "amount": 15.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include": False,
                "original_tax_ids": [(6, 0, [cls.tax_1.id])],
                "tax_group_id": cls.tax_group.id,
            }
        )
        cls.fiscal_position_0 = cls.env["account.fiscal.position"].create(
            {
                "name": "Default",
            }
        )
        cls.fiscal_position_1 = cls.env["account.fiscal.position"].create(
            {
                "name": "Business",
                "tax_ids": [(6, 0, [cls.tax_2.id])],
            }
        )
        cls.pricelist_1 = cls.env["product.pricelist"].create(
            {
                "name": "Business Pricelist",
                "currency_id": cls.env.ref("base.USD").id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "base": "list_price",
                            "compute_price": "percentage",
                            "percent_price": 20.0,
                        },
                    )
                ],
            }
        )
        cls.template = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "list_price": 750.0,
            }
        )
        cls.variant = cls.template.product_variant_ids[0]
        cls.template.taxes_id = cls.tax_1
        cls.env.user.company_id.currency_id = cls.env.ref("base.USD")
        cls.base_pricelist = cls.env["product.pricelist"].create(
            {"name": "Base Pricelist", "currency_id": cls.env.ref("base.USD").id}
        )
        cls.base_pricelist.currency_id = cls.env.ref("base.USD")
        cls.variant.currency_id = cls.env.ref("base.USD")

    def test_product_simple_get_price(self):
        self.variant.taxes_id.price_include = True
        self.assertEqual(
            self.variant._get_price(),
            {
                "discount": 0.0,
                "original_value": 750.0,
                "tax_included": True,
                "value": 750.0,
            },
        )
        self.variant.taxes_id.price_include = False
        self.assertEqual(
            self.variant._get_price(),
            {
                "discount": 0.0,
                "original_value": 750.0,
                "tax_included": False,
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
        fiscal_position_fr = self.fiscal_position_0
        self.variant.taxes_id.price_include = True
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
        promotion_price_list = self.pricelist_1
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
        tax_exclude_fiscal_position = self.fiscal_position_1
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
        self.env["product.pricelist.item"].create(
            {
                "product_id": self.variant.id,
                "pricelist_id": self.base_pricelist.id,
                "fixed_price": 10,
            }
        )
        fiscal_position_fr = self.fiscal_position_0
        self.variant.taxes_id.price_include = True
        price = self.variant.with_context(foo=1)._get_price(
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

    # FIXME v18 we cannot use `_show_discount` method
    # because it relies on `sale.group_discount_per_so_line` from sale module.
    # See https://github.com/odoo/odoo/issues/202035
    # The test should be updated when the issue is fixed to use
    # self.env.user.groups_id |= self.env.ref("sale.group_discount_per_so_line")
    def test_product_get_price_per_qty(self):
        PlItem = type(self.env["product.pricelist.item"])
        self.variant.taxes_id.price_include = True
        # Define a promotion price for the product with min_qty = 10
        fposition = self.fiscal_position_0
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
        with mock.patch.object(
            PlItem, "_show_discount", return_value=False, create=True
        ):
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
        PlItem = type(self.env["product.pricelist.item"])
        self.variant.taxes_id.price_include = True
        # Ensure that discount is with 2 digits
        self.env.ref("product.decimal_discount").digits = 2
        # self.base_pricelist doesn't define a tax mapping. We are tax included
        # Discount policy: do not show the discount.
        fiscal_position_fr = self.fiscal_position_0
        with mock.patch.object(
            PlItem, "_show_discount", return_value=False, create=True
        ):
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
        # Discount policy: show the discount.
        promotion_price_list = self.pricelist_1
        with mock.patch.object(
            PlItem, "_show_discount", return_value=True, create=True
        ):
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
        tax_exclude_fiscal_position = self.fiscal_position_1
        with mock.patch.object(
            PlItem, "_show_discount", return_value=False, create=True
        ):
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
        with mock.patch.object(
            PlItem, "_show_discount", return_value=True, create=True
        ):
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
        # Test the zero-discount branch: show_discount=True but pricelist computes
        # the same price as lst_price (original == pricelist price) → discount = 0.00
        pricelist_nodiscount = self.env["product.pricelist"].create(
            {
                "name": "Zero Discount Pricelist",
                "currency_id": self.env.ref("base.USD").id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "base": "list_price",
                            "compute_price": "percentage",
                            "percent_price": 0.0,  # 0% discount → same price as list
                        },
                    )
                ],
            }
        )
        with mock.patch.object(
            PlItem, "_show_discount", return_value=True, create=True
        ):
            price = self.variant._get_price(
                pricelist=pricelist_nodiscount, fposition=fiscal_position_fr
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
