# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,invalid-name
from odoo.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(TestProductCode, self).setUp()
        self.product_model = self.env['product.product']
        fields_get = self.product_model.fields_get()
        product_vals = self.product_model.default_get(fields_get.keys())
        product_vals['name'] = "My nice test product"
        product_vals['default_code'] = 'TST001'
        self.product = self.product_model.create(product_vals)

    def test_product_name_get(self):
        """Name get should return product name without code."""
        product_name = self.product.name_get()[0][1]
        self.assertEqual(product_name, self.product.name)
