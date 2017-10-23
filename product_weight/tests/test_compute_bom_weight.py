# -*- coding: utf-8 -*-
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBomWeightCompute(TransactionCase):

    def setUp(self):
        super(TestBomWeightCompute, self).setUp()
        self.bom = self.env.ref('mrp.mrp_bom_desk')
        self.component_1 = self.env.ref(
            'mrp.product_product_computer_desk_head')
        self.component_2 = self.env.ref(
            'mrp.product_product_computer_desk_leg')
        self.component_3 = self.env.ref(
            'mrp.product_product_computer_desk_bolt')
        self.product = self.env.ref('mrp.product_product_computer_desk')
        self.component_1.weight = 0.20
        self.component_2.weight = 0.22
        self.component_3.weight = 0.68
        self.variant1 = self.env.ref('product.product_product_11')
        self.variant2 = self.env.ref('product.product_product_11b')
        self.wiz_obj = self.env['product.weight.update']

    def test_calculate_product_weight_from_template_form(self):
        wizard = self.wiz_obj.with_context(
            active_model='product.template',
            active_id=self.product.product_tmpl_id.id).create({})
        wizard.update_single_weight()
        self.assertEqual(self.product.weight, 3.8)
        self.assertEqual(self.product.product_tmpl_id.weight, 3.8)

    def test_calculate_product_weight_from_product_form(self):
        wizard = self.wiz_obj.with_context(
            active_model='product.product',
            active_id=self.product.id).create({})
        wizard.update_single_weight()
        self.assertEqual(self.product.weight, 3.8)
        self.assertEqual(self.product.product_tmpl_id.weight, 3.8)

    def test_calculate_weight_from_template_tree(self):
        self.bom.product_tmpl_id = self.variant1.product_tmpl_id.id
        self.bom.product_id = self.variant1.id
        wizard = self.wiz_obj.with_context(
            active_model='product.template',
            active_ids=[self.variant1.product_tmpl_id.id]).create({})
        wizard.update_multi_product_weight()
        # You can't update template weight if it as variants
        self.assertEqual(self.variant1.product_tmpl_id.weight, 0.0)

    def test_calculate_weight_from_product_tree(self):
        self.bom.product_tmpl_id = self.variant1.product_tmpl_id.id
        self.bom.product_id = self.variant1.id
        wizard = self.wiz_obj.with_context(
            active_model='product.product',
            active_ids=[self.variant1.id, self.variant2.id]).create({})
        wizard.update_multi_product_weight()
        self.assertEqual(self.variant1.weight, 3.8)
        self.assertEqual(self.variant2.weight, 0.0)
