# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

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
                    'sequence': 1,
                }),
                (0, 0, {
                    'name': cls.supplier2.id,
                    'min_qty': 1,
                    'price': 10,
                    'sequence': 2,
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
            self.pricelist.get_product_price(self.product, 1, False), 50,
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
                self.product, 5, False, date='2019-01-01',
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
