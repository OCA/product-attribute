# -*- coding: utf-8 -*-
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    def setUp(self):
        super(TestProductSequence, self).setUp()
        self.product_product = self.env['product.product']

    def test_product_create_with_default_code(self):
        product_id = self.product_product.create(dict(
            name="Apple",
            default_code='PROD01'
        ))
        self.assertEqual(product_id.default_code, 'PROD01')

    def test_product_create_without_default_code(self):
        product_id_1 = self.product_product.create(dict(name="Orange"))
        self.assertRegexpMatches(str(product_id_1.default_code), r'PR/*')
