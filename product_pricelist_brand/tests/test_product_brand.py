# Copyright 2020 NextERP Romania SRL
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProductBrand(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductBrand, cls).setUpClass()
        cls.partner_obj = cls.env['res.partner']
        cls.brand_obj = cls.env['product.brand']
        cls.partner = cls.partner_obj.create({
            'name': 'Partner Test',
        })
        cls.brand = cls.brand_obj.create({
            'name': 'Brand Test',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'product_brand_id': cls.brand.id,
            'categ_id': cls.env.ref('product.product_category_all').id,
            'list_price': 100
        })
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Brand Pricelist',
            'item_ids': [
                (0, 0, {
                    'compute_price': 'formula',
                    'applied_on': '2_product_brand',
                    'brand_id': cls.brand.id,
                    'price_discount': 10,
                    'min_quantity': 1.0,
                }),
                (0, 0, {
                    'compute_price': 'formula',
                    'applied_on': '2_product_brand',
                    'brand_id': cls.brand.id,
                    'price_discount': 20,
                    'min_quantity': 5.0,
                }),
            ],
        })
        cls.item = cls.pricelist.item_ids.filtered(
            lambda r: r.price_discount == 10)
        cls.item_qty = cls.pricelist.item_ids.filtered(
            lambda r: r.price_discount == 20)

    def test_pricelist_based_on_product_category(self):
        self.item.write({
            'price_discount': 50,
            'applied_on': '2_product_category',
            'categ_id': self.env.ref('product.product_category_all').id,
            'brand_id': False,
        })
        self.item._onchange_applied_on()
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 50.0,
        )

    def test_pricelist_based_on_product(self):
        self.item.write({
            'price_discount': 30,
            'applied_on': '1_product',
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'brand_id': False,
        })
        self.item._onchange_applied_on()
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 70.0,
        )
        self.assertAlmostEqual(
            self.product.product_tmpl_id.with_context(
                pricelist=self.pricelist.id).price, 70.0,
        )

    def test_pricelist_based_on_product_variant(self):
        self.item.write({
            'price_discount': 25,
            'applied_on': '0_product_variant',
            'product_id': self.product.id,
            'brand_id': False,
        })
        self.item._onchange_applied_on()
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 75,
        )
        self.assertAlmostEqual(
            self.product.with_context(pricelist=self.pricelist.id).price, 75,
        )

    def test_pricelist_min_quantity(self):
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 1, False), 90,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 5, False), 80,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(self.product, 10, False), 80,
        )

    def test_pricelist_dates(self):
        """ Test pricelist and brand dates """
        self.item_qty.write({
            'date_start': '2018-12-31',
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product, 5, False, date='2019-01-01',
            ), 80,
        )
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product, 5, False, date='2017-01-01',
            ), 90,
        )
        self.item.write({
            'date_start': '2018-12-31',
        })
        self.assertAlmostEqual(
            self.pricelist.get_product_price(
                self.product, 5, False, date='2017-01-01',
            ), 100,
        )
