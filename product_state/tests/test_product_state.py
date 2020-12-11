# Copyright 2020 Hunki Enterprises BV (<https://hunki-enterprises.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestProductState(TransactionCase):
    def test_product_state(self):
        product = self.env['product.product'].search([], limit=1)
        product.state = 'end'
        self.assertEqual(
            product.product_state_id,
            self.env.ref('product_state.product_state_end'),
        )
        product.product_state_id = False
        self.assertFalse(product.state)
