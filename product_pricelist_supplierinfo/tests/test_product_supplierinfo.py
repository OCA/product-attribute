# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date

from odoo.tests import common


class TestProductSupplierinfo(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductSupplierinfo, cls).setUpClass()
        cls.partner_obj = cls.env['res.partner']
        cls.partner = cls.partner_obj.create({
            'name': 'Partner Test',
        })
        cls.supplier1 = cls.partner_obj.create({
            'name': 'Supplier #1',
        })
        cls.supplier2 = cls.partner_obj.create({
            'name': 'Supplier #2',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'seller_ids': [
                (0, 0, {
                    'name': cls.supplier1.id,
                    'min_qty': 5,
                    'price': 50,
                }),
                (0, 0, {
                    'name': cls.supplier2.id,
                    'min_qty': 1,
                    'price': 10,
                }),
            ],
        })
        cls.product_with_diff_uom = cls.env['product.product'].create({
            'name': 'Product UOM Test',
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'uom_po_id': cls.env.ref('uom.product_uom_dozen').id,
            'seller_ids': [
                (0, 0, {
                    'name': cls.supplier1.id,
                    'min_qty': 1,
                    'price': 1200,
                }),
            ],
        })
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Supplierinfo Pricelist',
            'item_ids': [
                (0, 0, {
                    'compute_price': 'formula',
                    'base': 'supplierinfo',
                    'price_discount': 0,
                    'min_quantity': 1.0,
                }),
            ],
        })

    def test_pricelist_based_on_product_category(self):
        self.pricelist.item_ids[0].write({
            'price_discount': 50,
            'applied_on': '2_product_category',
            'categ_id': self.env.ref('product.product_category_all').id,
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 5.0,
        )

    def test_pricelist_based_on_product(self):
        self.pricelist.item_ids[0].write({
            'applied_on': '1_product',
            'product_tmpl_id': self.product.product_tmpl_id.id,
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 10.0,
        )
        self.assertAlmostEqual(
            self.product.product_tmpl_id.with_context(
                pricelist=self.pricelist.id).price, 10.0,
        )

    def test_pricelist_based_on_product_variant(self):
        self.pricelist.item_ids[0].write({
            'price_discount': -25,
            'applied_on': '0_product_variant',
            'product_id': self.product.id,
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 12.5,
        )
        self.assertAlmostEqual(
            self.product.with_context(pricelist=self.pricelist.id).price, 12.5,
        )

    def test_pricelist_min_quantity(self):
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 10,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False), 50,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 10, False), 50,
        )
        self.pricelist.item_ids[0].no_supplierinfo_min_quantity = True
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False), 10,
        )

    def test_pricelist_supplier_filter(self):
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False), 50,
        )
        self.pricelist.item_ids[0].filter_supplier_id = self.supplier2.id
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False), 10,
        )

    def test_pricelist_dates(self):
        """ Test pricelist and supplierinfo dates """
        self.product.seller_ids.filtered(
            lambda x: x.min_qty == 5
        )[0].date_start = '2018-12-31'
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product, 5, False, date=date(2019, 1, 1),
            ), 50,
        )

    def test_pricelist_based_price_round(self):
        self.pricelist.item_ids[0].write({
            'price_discount': 50,
            'applied_on': '2_product_category',
            'price_round': 1,
            'price_surcharge': 5,
            'price_min_margin': 10,
            'price_max_margin': 100,
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 20.0,
        )

    def test_pricelist_based_on_sale_margin(self):
        self.pricelist.item_ids[0].write({
            'applied_on': '1_product',
            'product_tmpl_id': self.product.product_tmpl_id.id,
        })
        seller = self.product.seller_ids[0]
        seller.sale_margin = 50
        self.assertAlmostEqual(
            seller._get_supplierinfo_pricelist_price(), 75.0,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 6, False), 75.0,
        )
        self.assertAlmostEqual(
            self.product.product_tmpl_id.with_context(
                pricelist=self.pricelist.id, quantity=6).price, 75.0,
        )

    def test_supplierinfo_per_variant(self):
        tmpl = self.env['product.template'].create({
            'name': 'Test Product',
            'attribute_line_ids': [[0, 0, {
                'attribute_id': self.env.ref('product.product_attribute_1').id,
                'value_ids': [
                    (4, self.env.ref('product.product_attribute_value_1').id),
                    (4, self.env.ref('product.product_attribute_value_2').id),
                ],
            }]]
        })
        variant1 = tmpl.product_variant_ids[0]
        variant2 = tmpl.product_variant_ids[1]
        tmpl.write({'seller_ids': [
            (0, 0, {
                'name': self.supplier1.id,
                'product_id': variant1.id,
                'price': 15,
            }),
            (0, 0, {
                'name': self.supplier1.id,
                'product_id': variant2.id,
                'price': 25,
            }),
        ]})
        self.assertAlmostEqual(
            self.pricelist.get_product_price(variant1, 1, False), 15.0,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(variant2, 1, False), 25.0,
        )

    def test_pricelist_and_supplierinfo_currencies(self):
        """Test when we have 2 records of supplierinfo in two currencies, on a same
        pricelist as pricelist items, the currency on the supplier that have a
        different currency will be converted to the pricelist's currency.
        """
        # Setting the currencies and rates for the test, so we can have a supplierinfo
        # and pricelist with different currencies
        currency_usd = self.env.ref('base.USD')
        currency_mxn = self.env.ref('base.MXN')
        self.env['res.currency.rate'].create({
            'currency_id': currency_usd.id,
            'rate': 1,
            'name': date.today()
        })
        self.env['res.currency.rate'].create({
            'currency_id': currency_mxn.id,
            'rate': 20,
            'name': date.today()
        })

        # Setting the item with the product
        self.pricelist.item_ids[0].write({
            'applied_on': '0_product_variant',
            'product_id': self.product.id,
        })
        self.product.seller_ids[0].currency_id = currency_mxn
        self.pricelist.currency_id = currency_usd

        product_seller_price = self.product.seller_ids[0].price
        product_pricelist_price = self.pricelist.get_product_price(
            self.product, 5, False)
        # The price with MXN Currency will be 50 as is set in the setup
        self.assertEqual(product_seller_price, 50)
        # And the price with the pricelist  (USD Currency) will be 2.5
        self.assertEqual(product_pricelist_price, 2.5)

    def test_line_uom_and_supplierinfo_uom(self):
        """Test when we have a product is sold in a different uom from the one on set
        for purchase.
        """
        # Setting the item with the product
        self.pricelist.item_ids[0].write({
            'applied_on': '0_product_variant',
            'product_id': self.product_with_diff_uom.id,
            'price_discount': -20,
        })

        product_seller_price = self.product_with_diff_uom.seller_ids[0].price
        uom_dozen = self.env.ref('uom.product_uom_dozen')
        product_pricelist_price_dozen = self.pricelist.get_product_price(
            self.product_with_diff_uom.with_context(uom=uom_dozen.id), 1, False)
        uom_unit = self.env.ref('uom.product_uom_unit')
        product_pricelist_price_unit = self.pricelist.get_product_price(
            self.product_with_diff_uom.with_context(uom=uom_unit.id), 1, False)
        # The price with the will be 1200 on the seller (1 Dozen)
        self.assertEqual(product_seller_price, 1200)

        # The price with the will be 1200 plus the increment of the 20% which will
        # give us a total of 1440 (1 Dozen)
        self.assertEqual(product_pricelist_price_dozen, 1440)

        # And the price with the pricelist and the uom of Units (Instead of Dozen)
        # will be 100, plus the 20% the total will be 120 per Unit
        self.assertEqual(product_pricelist_price_unit, 120)
