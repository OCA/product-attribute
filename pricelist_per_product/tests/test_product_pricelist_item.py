# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductPricelistItem(TransactionCase):

    def setUp(self):
        super(TestProductPricelistItem, self).setUp()
        self.pricelist_data = {
            'applied_on': '0_product_variant',
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

    def test_applied_on_val(self):
        """ It should test that the right value of applied_on  field"""
        pricelist_item = self.pricelist_item.create(
            self.pricelist_data)
        self.assertEqual(pricelist_item.applied_on, '1_product')
        pricelist_item.write(self.pricelist_data_2)
        self.assertEqual(pricelist_item.applied_on, '0_product_variant')
