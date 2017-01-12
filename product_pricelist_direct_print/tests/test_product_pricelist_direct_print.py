# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import SavepointCase


class TestProductPricelistDirectPrint(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductPricelistDirectPrint, cls).setUpClass()
        cls.pricelist = cls.env.ref('product.list0')
        cls.category = cls.env['product.category'].create({
            'name': 'Test category',
            'type': 'normal',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product for test',
            'categ_id': cls.category.id,
            'default_code': 'TESTPROD01',
        })
        cls.wiz_obj = cls.env['product.pricelist.print']

    def test_defaults(self):
        wiz = self.wiz_obj.new()
        res = wiz.with_context(
            active_model='product.pricelist',
            active_id=self.pricelist.id,
        ).default_get([])
        self.assertEqual(res['pricelist_id'], self.pricelist.id)
        res = wiz.with_context(
            active_model='product.template',
            active_ids=self.product.product_tmpl_id.ids,
        ).default_get([])
        self.assertEqual(
            res['product_tmpl_ids'][0][2], self.product.product_tmpl_id.ids)
        res = wiz.with_context(
            active_model='product.product',
            active_ids=self.product.ids,
        ).default_get([])
        self.assertEqual(
            res['product_ids'][0][2], self.product.ids)
        self.assertTrue(res['show_variants'])

        res = wiz.print_report()
        self.assertIn('report_name', res)
