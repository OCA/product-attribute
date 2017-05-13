# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestHooks(TransactionCase):

    def test_find_templates_with_imgs_custom(self):
        """ Test tmpls with imgs set to custom img_type """
        earphones = self.env.ref('product.product_product_7_product_template')
        self.assertEquals(
            earphones.img_type,
            'custom',
        )

    def test_find_templates_with_imgs_no_image(self):
        """ Test tmpls without imgs left as no_image """
        computer = self.env.ref('product.consu_delivery_03_product_template')
        self.assertEquals(
            computer.img_type,
            'no_image',
        )
