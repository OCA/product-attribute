# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductPricelist(TransactionCase):

    def setUp(self):
        super(TestProductPricelist, self).setUp()
        self.pricelist = self.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'currency_id': self.env.ref('base.USD').id,
        })
        self.pricelist_item = self.env['product.pricelist.item'].create({
            'applied_on': '1_product',
            'base': 'list_price',
            'name': 'Test Pricelist Item',
            'pricelist_id': self.pricelist.id,
            'product_tmpl_id': self.env.ref('product.product_product_4').id,
            'sequence': 5,
        })

    def test_compute_product_template_count(self):
        """ It should test that the right template count is returned """
        self.pricelist._compute_product_template_count()
        self.assertTrue(self.pricelist.product_template_count == 1)

    def test_button_template_in_pricelist(self):
        """ It should return a view with a domain for the products in the
            pricelist """
        pids = self.env.ref('product.product_product_4').ids
        exp = {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', pids)],
            'view_mode': 'tree,form',
            'res_model': 'product.template',
        }
        res = self.pricelist.button_template_in_pricelist()
        self.assertEqual(exp, res)
