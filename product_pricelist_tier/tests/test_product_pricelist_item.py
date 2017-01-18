# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestPricelistItem(TransactionCase):

    def setUp(self):
        super(TestPricelistItem, self).setUp()
        self.pricelist_item = self.env.ref(
            'product_pricelist_tier.'
            'product_pricelist_item_item_tiered'
        )
        self.toy = self.env.ref(
            'product_pricelist_tier.'
            'product_template_plastic_toy'
        )

    def test_tiered_price_0_if_not_tiered(self):
        """ Test tiered price 0 if not applied on product """
        self.pricelist_item.compute_price = 'fixed'
        self.pricelist_item.applied_on = '3_global'
        self.pricelist_item._onchange_compute_price()
        self.assertEquals(
            self.pricelist_item.tiered_price,
            0.0,
        )

    def test_base_set_to_list_price_if_tiered(self):
        """ Test base set to list_price if tiered """
        self.pricelist_item.base = 'standard_price'
        self.pricelist_item._onchange_price_discount()
        self.assertEquals(
            self.pricelist_item.base,
            'list_price',
        )

    def test_tiered_price_not_on_product(self):
        """ Test raise ValidationError if not on product """
        with self.assertRaises(ValidationError):
            self.pricelist_item.applied_on = '3_global'

    def test_constrains_min_quantity_none(self):
        """ Test raise ValidationError if tiered and none min_quantity """
        with self.assertRaises(ValidationError):
            self.pricelist_item.min_quantity = 0

    def test_tiered_price_calculated(self):
        """ Test percent discount correct """
        self.pricelist_item._onchange_price_discount()
        self.assertEquals(
            self.pricelist_item.price_discount,
            20.0,
        )

    def test_tiered_price_no_list_price(self):
        """ Test price_discount is 0 if no product list_price """
        self.toy.list_price = 0.0
        self.pricelist_item._onchange_price_discount()
        self.assertEquals(
            self.pricelist_item.price_discount,
            0.0,
        )
