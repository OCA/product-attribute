import json
from odoo.tests import Form, TransactionCase


class TestProductLifecycle(TransactionCase):

    def setUp(self):
        super(TestProductLifecycle, self).setUp()
        self.doble_obsolete_product = self.env.ref('product.product_product_4d')
        self.obsolete_replacement = self.env.ref('product_lifecycle.product_product_4f')
        self.good_replacement = self.env.ref('product_lifecycle.product_product_4g')
        self.end_product = self.env.ref('product.product_product_6')
        self.customer = self.env.ref('base.res_partner_2')

    def test_01_product_suggestion(self):
        # Test good_replacement
        self.assertEqual(self.doble_obsolete_product.lifecycle_state, 'obsolete')
        self.assertEqual(self.obsolete_replacement.lifecycle_state, 'obsolete')
        self.assertFalse(self.good_replacement.lifecycle_state == 'obsolete')
        self.assertEqual(self.doble_obsolete_product.replaced_by_product_id,
                         self.obsolete_replacement)
        self.assertEqual(self.doble_obsolete_product.get_good_replacements(),
                         self.good_replacement)
        self.assertEqual(self.obsolete_replacement.get_good_replacements(),
                         self.good_replacement)

    def test_02_so_suggestion(self):
        # Show widget info
        order_form = Form(self.env['sale.order'])
        order_form.partner_id = self.customer
        with order_form.order_line.new() as line:
            line.product_id = self.doble_obsolete_product
        sale_order = order_form.save()
        so_line = sale_order.order_line[0]
        self.assertTrue(so_line.show_replacement)
        widget_info = json.loads(so_line.replacement_info_widget)
        self.assertEqual(widget_info['product_id'], self.good_replacement.id)
        # No show widget
        order_form = Form(self.env['sale.order'])
        order_form.partner_id = self.customer
        with order_form.order_line.new() as line:
            line.product_id = self.good_replacement
        sale_order = order_form.save()
        so_line = sale_order.order_line[0]
        self.assertFalse(so_line.show_replacement)

    def test_03_product_write(self):
        self.doble_obsolete_product.write({'lifecycle_state': 'end'})
        self.assertEqual(self.doble_obsolete_product.lifecycle_state, 'obsolete')
        self.end_product.write({'lifecycle_state': 'obsolete'})
        self.assertEqual(self.end_product.lifecycle_state, 'end')

    def test_04_update_product_state(self):
        # confirm picking for product in end
        pickings = self.env['stock.picking'].search([
            ('move_lines.product_id', '=', self.end_product.id),
            ('state', 'not in', ('done', 'draft', 'cancelled'))])
        ready = pickings.filtered(lambda p: p.state == 'assigned')
        for pick in ready:
            for move in pick.move_lines:
                move.write({'quantity_done': move.product_uom_qty})
            pick.button_validate()
        for pick in pickings - ready:
            pick.action_assign()
            for move in pick.move_lines:
                move.write({'quantity_done': move.product_uom_qty})
            pick.button_validate()
        # sold qty available
        order_form = Form(self.env['sale.order'])
        order_form.partner_id = self.customer
        with order_form.order_line.new() as line:
            line.product_id = self.end_product
            line.product_uom_qty = self.end_product.qty_available
        sale_order = order_form.save()
        sale_order.action_confirm()
        sale_order.picking_ids.move_lines.write({
            'quantity_done': self.end_product.qty_available})
        sale_order.picking_ids.button_validate()
        # check method to update state
        self.assertEqual(sale_order.picking_ids.state, 'done')
        self.assertEqual(self.end_product.lifecycle_state, 'end')
        self.end_product.update_product_state()
        self.assertEqual(self.end_product.lifecycle_state, 'obsolete')
