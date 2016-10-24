# -*- coding: utf-8 -*-
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from ..hooks import pre_init_hook


class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    def setUp(self):
        super(TestProductSequence, self).setUp()
        self.product_product = self.env['product.product']

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
