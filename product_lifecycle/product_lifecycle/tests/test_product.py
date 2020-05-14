# Copyright 2019 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import json
from odoo.tests import Form, TransactionCase


class TestProductLifecycle(TransactionCase):

    def setUp(self):
        super(TestProductLifecycle, self).setUp()
        self.doble_obsolete_product = self.env.ref('product.product_product_4d')
        self.obsolete_replacement = self.env.ref('product_lifecycle.product_product_4f')
        self.good_replacement = self.env.ref('product_lifecycle.product_product_4g')
        self.customer = self.env.ref('base.res_partner_2')

    def test_01_product_suggestion(self):
        # Test good_replacement
        self.assertEqual(self.doble_obsolete_product.lifecycle_state, 'obsolete')
        self.assertEqual(self.obsolete_replacement.lifecycle_state, 'obsolete')
        self.assertFalse(self.good_replacement.lifecycle_state == 'obsolete')
        self.assertEqual(self.doble_obsolete_product.replaced_by_product_id, self.obsolete_replacement)
        self.assertEqual(self.doble_obsolete_product.get_good_replacements(), self.good_replacement)
        self.assertEqual(self.obsolete_replacement.get_good_replacements(), self.good_replacement)

    def test_02_so_suggestion(self):
        order_form = Form(self.env['sale.order'])
        order_form.partner_id = self.customer
        with order_form.order_line.new() as line:
            line.product_id = self.doble_obsolete_product
        sale_order = order_form.save()
        so_line = sale_order.order_line[0]
        self.assertTrue(so_line.show_replacement)
        widget_info = json.loads(so_line.replacement_info_widget)
        self.assertEqual(widget_info['product_id'], self.good_replacement.id)
