# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase

from ..image_constants import (
    NONE,
    CUSTOM,
)


class TestHooks(TransactionCase):

    def test_find_templates_with_imgs_custom(self):
        """ Test tmpls with imgs set to custom image_type """
        earphones = self.env.ref('product.product_product_7_product_template')
        self.assertEquals(
            earphones.image_type,
            CUSTOM,
        )

    def test_find_templates_with_imgs_none(self):
        """ Test tmpls without imgs left as none """
        computer = self.env.ref('product.consu_delivery_03_product_template')
        self.assertEquals(
            computer.image_type,
            NONE,
        )
