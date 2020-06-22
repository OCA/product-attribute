# -*- coding: utf-8 -*-
# Copyright 2019 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests.common as common


class TestProductSupplierinfoRebate(common.TransactionCase):

    def setUp(self):
        super(TestProductSupplierinfoRebate, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        self.product = self.env.ref('product.product_product_4')
        self.partner = self.env.ref('base.res_partner_2')
        self.company = self.env.ref('base.main_company')

        self.supplierinfo = self.env['product.supplierinfo'].create({
            'name': self.partner.id,
            'product_id': self.product.id,
            'product_code': '00001',
            'price': 100.0,
            'rebate_price': 50.0,
        })

    def test_product_supplierinfo_rebate(self):
        self.assertEqual(self.supplierinfo.rebate_discount, 50.0,
                         "Bad rebate discount")
        self.assertEqual(self.supplierinfo.rebate_multiplied, 0.5,
                         "Bad rebate mult")
