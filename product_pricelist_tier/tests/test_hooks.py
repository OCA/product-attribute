# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHooks(TransactionCase):

    def setUp(self):
        super(TestHooks, self).setUp()
        self.pricelist_item = self.env.ref(
            'product_pricelist_tier.'
            'product_pricelist_item_item_tiered'
        )

    def test_post_init_hook(self):
        """ Test hook triggers onchange price discount """
        self.assertEquals(
            self.pricelist_item.price_discount,
            20.00,
        )
