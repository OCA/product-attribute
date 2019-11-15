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

    def test_onchange_compute_price(self):
        """ Test tiered price 0 if not applied on product """
        self.pricelist_item.compute_price = 'fixed'
        self.pricelist_item.applied_on = '3_global'
        self.pricelist_item._onchange_compute_price()
        self.assertEquals(
            self.pricelist_item.tiered_price,
            0.0,
        )

    def test_check_tier_validations_min_quantity(self):
        """ Test raise ValidationError if tiered and none min_quantity """
        with self.assertRaises(ValidationError):
            self.pricelist_item.min_quantity = 0

    def test_check_tier_validations_applied_on(self):
        """ Test raise ValidationError if not applied on product """
        with self.assertRaises(ValidationError):
            self.pricelist_item.applied_on = '3_global'

    def test_check_tier_validations_base(self):
        """ Test raise ValidationError if not based on list_price """
        with self.assertRaises(ValidationError):
            self.pricelist_item.base = 'standard_price'

    def test_onchange_price_discount(self):
        """ Test percent discount correct """
        self.pricelist_item._onchange_price_discount()
        self.assertEquals(
            self.pricelist_item.price_discount,
            20.0,
        )

    def test_onchange_price_discount_no_list_price(self):
        """ Test price_discount is 0 if no product list_price """
        self.toy.list_price = 0.0
        self.pricelist_item._onchange_price_discount()
        self.assertEquals(
            self.pricelist_item.price_discount,
            0.0,
        )
