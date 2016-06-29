# -*- coding: utf-8 -*-
# © 2016 initOS GmbH.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestProductUniqueDefaultCode(TransactionCase):

    def setUp(self):
        super(TestProductUniqueDefaultCode, self).setUp()

        self.model = self.env['product.product']

    def test_1(self):
        self.product = self.model.create(
            {
                'name': 'product1',
                'default_code': 'product1'
            }
        )
        self.assertEqual(
            'product1',
            self.product.default_code
        )

    def test_2(self):
        with self.assertRaises(UserError):
            self.product = self.model.create(
                {
                    'name': 'product2',
                    'default_code': 'product1'
                }
            )
