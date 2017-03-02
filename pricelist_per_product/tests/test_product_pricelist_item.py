# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductPricelistItem(TransactionCase):

    def setUp(self):
        super(TestProductPricelistItem, self).setUp()
        self.pricelist_data = {
            'applied_on': '1_product',
            'base': 'list_price',
            'name': 'Test Pricelist Item',
            'product_tmpl_id': self.env.ref('product.product_product_4').id,
            'sequence': 5,
        }
        self.pricelist_data_2 = {
            'applied_on': '1_product',
            'base': 'list_price',
            'name': 'Test Pricelist Item',
            'product_id': self.env.ref('product.product_product_4').id,
            'sequence': 5,
        }
        self.pricelist_item = self.env['product.pricelist.item']

    def test_get_sequence_price_grid_template(self):
        """ It should test that the right sequence number is returned
         for pricelists with a template """
        sequence = self.pricelist_item._get_sequence_price_grid(
            self.pricelist_data
        )
        self.assertTrue(sequence == 10)

    def test_get_sequence_price_grid_variant(self):
        """ It should test that the right sequence number is returned
         for pricelists with a variant """
        sequence = self.pricelist_item._get_sequence_price_grid(
            self.pricelist_data_2
        )
        self.assertTrue(sequence == 5)
