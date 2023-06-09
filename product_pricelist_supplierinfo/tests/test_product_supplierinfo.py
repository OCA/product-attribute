# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date

from odoo.tests import common


class TestProductSupplierinfo(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_obj = cls.env["res.partner"]
        cls.currency_rate_obj = cls.env["res.currency.rate"]
        cls.partner = cls.partner_obj.create({"name": "Partner Test"})
        cls.supplier1 = cls.partner_obj.create({"name": "Supplier #1"})
        cls.supplier2 = cls.partner_obj.create({"name": "Supplier #2"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "seller_ids": [
                    (0, 0, {"name": cls.supplier1.id, "min_qty": 5, "price": 50}),
                    (0, 0, {"name": cls.supplier2.id, "min_qty": 1, "price": 10}),
                ],
            }
        )
        cls.product_with_diff_uom = cls.env["product.product"].create(
            {
                "name": "Product UOM Test",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_dozen").id,
                "seller_ids": [
                    (0, 0, {"name": cls.supplier1.id, "min_qty": 1, "price": 1200}),
                ],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Supplierinfo Pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "formula",
                            "base": "supplierinfo",
                            "price_discount": 0,
                            "min_quantity": 1.0,
                        },
                    ),
                ],
            }
        )

    @classmethod
    def _update_rate(cls, currency_id, rate):
        currency_rate = cls.currency_rate_obj.search(
            [("name", "=", date.today()), ("currency_id", "=", currency_id.id)], limit=1
        )
        if not currency_rate:
            cls.currency_rate_obj.create(
                {"currency_id": currency_id.id, "rate": rate, "name": date.today()}
            )
        else:
            currency_rate.write({"rate": rate})

    def test_pricelist_based_on_product_category(self):
        self.pricelist.item_ids[0].write(
            {
                "price_discount": 50,
                "applied_on": "2_product_category",
                "categ_id": self.env.ref("product.product_category_all").id,
            }
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            5.0,
        )

    def test_pricelist_based_on_product(self):
        self.pricelist.item_ids[0].write(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product.product_tmpl_id, 1, False),
            10.0,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            10.0,
        )
        self.assertAlmostEqual(
            self.product.product_tmpl_id.with_context(
                pricelist=self.pricelist.id
            ).price,
            10.0,
        )

    def test_pricelist_based_on_product_variant(self):
        self.pricelist.item_ids[0].write(
            {
                "price_discount": -25,
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
            }
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            12.5,
        )
        self.assertAlmostEqual(
            self.product.with_context(pricelist=self.pricelist.id).price,
            12.5,
        )

    def test_pricelist_min_quantity(self):
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            10,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False),
            50,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 10, False),
            50,
        )
        self.pricelist.item_ids[0].no_supplierinfo_min_quantity = True
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False),
            10,
        )

    def test_pricelist_supplier_filter(self):
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False),
            50,
        )
        self.pricelist.item_ids[0].filter_supplier_id = self.supplier2.id
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False),
            10,
        )

    def test_pricelist_select_supplier(self):
        supplier3 = self.partner_obj.create({"name": "Supplier #3"})
        self.product.write(
            {"seller_ids": [(0, 0, {"name": supplier3.id, "min_qty": 1, "price": 9})]}
        )
        for seller_id in self.product.seller_ids:
            price = self.pricelist.with_context(
                supplier=seller_id.name.id
            ).get_product_price(
                product=seller_id.product_id or seller_id.product_tmpl_id,
                quantity=seller_id.min_qty,
                partner=False,
                uom_id=seller_id.product_uom.id,
            )
            self.assertEqual(price, seller_id.price)

    def test_pricelist_dates(self):
        """Test pricelist and supplierinfo dates"""

        # Set a start date for the supplier #1
        self.product.seller_ids.filtered(lambda x: x.min_qty == 5)[
            0
        ].date_start = "2018-12-31"
        # If today is before this date, supplier #1 is ignored and we fallback on
        # selecting supplier #2
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product,
                5,
                False,
                date=date(2018, 12, 30),
            ),
            10,
        )
        # If today is after this date, supplier #1 is selected
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product,
                5,
                False,
                date=date(2019, 1, 1),
            ),
            50,
        )
        # Now create a new and more interesting supplier offer (same min. quantities)
        # with a starting date already set
        supplier3 = self.partner_obj.create({"name": "Supplier #3"})
        self.product.write(
            {
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": supplier3.id,
                            "min_qty": 5,
                            "price": 45,
                            "date_start": "2019-01-02",
                        },
                    )
                ]
            }
        )
        # If today is before this date, supplier #3 is ignored and we fallback on
        # selecting supplier #1
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product,
                5,
                False,
                date=date(2019, 1, 1),
            ),
            50,
        )
        # If today is after this date, the new supplier #3 is selected
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product,
                5,
                False,
                date=date(2019, 1, 3),
            ),
            45,
        )

    def test_pricelist_based_price_round(self):
        self.pricelist.item_ids[0].write(
            {
                "price_discount": 50,
                "applied_on": "2_product_category",
                "categ_id": self.product.categ_id.id,
                "price_round": 1,
                "price_surcharge": 5,
                "price_min_margin": 10,
                "price_max_margin": 100,
            }
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False),
            20.0,
        )

    def test_pricelist_based_on_sale_margin(self):
        self.pricelist.item_ids[0].write(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        seller = self.product.seller_ids[0]
        seller.sale_margin = 50
        self.assertAlmostEqual(
            seller._get_supplierinfo_pricelist_price(),
            75.0,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 6, False),
            75.0,
        )
        self.assertAlmostEqual(
            self.product.product_tmpl_id.with_context(
                pricelist=self.pricelist.id, quantity=6
            ).price,
            75.0,
        )

    def test_supplierinfo_per_variant(self):
        tmpl = self.env["product.template"].create(
            {
                "name": "Test Product",
                "attribute_line_ids": [
                    [
                        0,
                        0,
                        {
                            "attribute_id": self.env.ref(
                                "product.product_attribute_1"
                            ).id,
                            "value_ids": [
                                (
                                    4,
                                    self.env.ref(
                                        "product.product_attribute_value_1"
                                    ).id,
                                ),
                                (
                                    4,
                                    self.env.ref(
                                        "product.product_attribute_value_2"
                                    ).id,
                                ),
                            ],
                        },
                    ]
                ],
            }
        )
        variant1 = tmpl.product_variant_ids[0]
        variant2 = tmpl.product_variant_ids[1]
        tmpl.write(
            {
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.supplier1.id,
                            "product_id": variant1.id,
                            "price": 15,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.supplier1.id,
                            "product_id": variant2.id,
                            "price": 25,
                        },
                    ),
                ]
            }
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(variant1, 1, False),
            15.0,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(variant2, 1, False),
            25.0,
        )

    def test_pricelist_and_supplierinfo_currencies(self):
        """Test when we have 2 records of supplierinfo in two currencies, on a same
        pricelist as pricelist items, the currency on the supplier that have a
        different currency will be converted to the pricelist's currency.
        """
        # Setting the currencies and rates for the test, so we can have a supplierinfo
        # and pricelist with different currencies
        currency_usd = self.env.ref("base.USD")
        currency_mxn = self.env.ref("base.MXN")
        self._update_rate(currency_usd, 1)
        self._update_rate(currency_mxn, 20)

        # Setting the item with the product
        self.pricelist.item_ids[0].write(
            {"applied_on": "0_product_variant", "product_id": self.product.id}
        )
        self.product.seller_ids[0].currency_id = currency_mxn
        self.pricelist.currency_id = currency_usd

        product_seller_price = self.product.seller_ids[0].price
        product_pricelist_price = self.pricelist.get_product_price(
            self.product, 5, False
        )
        # The price with MXN Currency will be 50 as is set in the setup
        self.assertEqual(product_seller_price, 50)
        # And the price with the pricelist  (USD Currency) will be 2.5
        self.assertEqual(product_pricelist_price, 2.5)

    def test_line_uom_and_supplierinfo_uom(self):
        """Test when we have a product is sold in a different uom from the one on set
        for purchase.
        """
        # Setting the item with the product
        self.pricelist.item_ids[0].write(
            {
                "applied_on": "0_product_variant",
                "product_id": self.product_with_diff_uom.id,
                "price_discount": -20,
                # Remember that formula's computed price is expressed in the
                # product's default UoM
                "price_surcharge": 3.0,
            }
        )

        product_seller_price = self.product_with_diff_uom.seller_ids[0].price
        # The price with the will be 1200 on the seller (1 Dozen)
        self.assertEqual(product_seller_price, 1200)

        uom_dozen = self.env.ref("uom.product_uom_dozen")
        product_pricelist_price_dozen = self.pricelist.with_context(
            uom=uom_dozen.id
        ).get_product_price(self.product_with_diff_uom, 1, False)
        # The price with the will be 1200 plus the increment of the 20% plus a
        # surcharge of 36 which will give us a total of 1476 (for 1 Dozen)
        self.assertEqual(product_pricelist_price_dozen, 1476)

        uom_unit = self.env.ref("uom.product_uom_unit")
        product_pricelist_price_unit = self.pricelist.with_context(
            uom=uom_unit.id
        ).get_product_price(self.product_with_diff_uom, 1, False)
        # And the price with the pricelist and the uom of Units (Instead of Dozen)
        # will be 100, plus the 20%, plus 3.0 of sucharge, the total will be 123 per
        # Unit
        self.assertEqual(product_pricelist_price_unit, 123)

        uom_half_dozen = self.env["uom.uom"].create(
            {
                "name": "Half-dozens",
                "category_id": self.env.ref("uom.product_uom_categ_unit").id,
                "factor_inv": 6.0,
                "uom_type": "bigger",
            }
        )
        product_pricelist_price_unit = self.pricelist.with_context(
            uom=uom_half_dozen.id
        ).get_product_price(self.product_with_diff_uom, 1, False)
        # And the price with the pricelist and the uom of Units (Instead of Dozen)
        # will be 100, plus the 20%, plus 3.0 of sucharge, the total will be 123 per
        # Unit
        self.assertEqual(product_pricelist_price_unit, 738)
