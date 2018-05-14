# -*- coding: utf-8 -*-
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from ..hooks import pre_init_hook


class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    def setUp(self):
        super(TestProductSequence, self).setUp()
        self.product_product = self.env['product.product']
        self.product_category = self.env['product.category']

    def test_product_create_with_default_code(self):
        product = self.product_product.create(dict(
            name="Apple",
            default_code='PROD01'
        ))
        self.assertEqual(product.default_code, 'PROD01')

    def test_product_create_without_default_code(self):
        product_1 = self.product_product.create(dict(
            name="Orange",
            default_code='/'))
        self.assertRegexpMatches(str(product_1.default_code), r'PR/*')

    def test_product_copy(self):
        product_2 = self.product_product.create(dict(
            name="Apple",
            default_code='PROD02'
        ))
        copy_product_2 = product_2.copy()
        self.assertEqual(copy_product_2.default_code, 'PROD02-copy')

    def test_pre_init_hook(self):
        product_3 = self.product_product.create(dict(
            name="Apple",
            default_code='PROD03'
        ))
        self.cr.execute(
            "update product_product set default_code='/' where id=%s"
            % (product_3.id,))
        product_3.invalidate_cache()
        self.assertEqual(product_3.default_code, '/')
        pre_init_hook(self.cr)
        product_3.invalidate_cache()
        self.assertEqual(product_3.default_code, '!!mig!!%s' % (product_3.id,))

    def test_product_category_sequence(self):
        categ_grocery = self.product_category.create(dict(
            name="Grocery",
            code_prefix="GRO",
        ))
        self.assertTrue(categ_grocery.sequence_id)
        self.assertEqual(categ_grocery.sequence_id.prefix, "GRO")
        self.assertFalse(categ_grocery.sequence_id.company_id)
        product_3 = self.product_product.create(dict(
            name="Apple",
            categ_id=categ_grocery.id,
        ))
        self.assertEqual(product_3.default_code[:3], "GRO")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "GRO")
        categ_electronics = self.product_category.create(dict(
            name="Electronics",
            code_prefix="ELE",
        ))
        product_3.write({'default_code': '/',
                         'categ_id': categ_electronics.id})
        self.assertEqual(product_3.default_code[:3], "ELE")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "ELE")
        categ_car = self.product_category.create(dict(
            name="Car",
            code_prefix="CAR",
        ))
        product_3.product_tmpl_id.categ_id = categ_car
        product_3.product_tmpl_id.default_code = '/'
        product_3.refresh()
        self.assertEqual(product_3.default_code[:3], "CAR")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "CAR")
        categ_car.write(dict(
            name="Bike",
            code_prefix="BIK",
        ))
        self.assertEqual(categ_car.sequence_id.prefix, "BIK")
        categ_car.sequence_id = False
        categ_car.write({'code_prefix': 'KIA'})
        self.assertEqual(categ_car.sequence_id.prefix, "KIA")
