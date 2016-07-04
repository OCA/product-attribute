# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestItemGenerator(TransactionCase):
    def test_to_update_field_to_false(self):
        """ Check if generator field 'to_update' is False
            after clicked on synchronize button """
        # click on button
        self.main_generator.build_pricelist_item()
        self.assertEqual(self.main_generator.to_update, False)

    def test_first_synchro_item(self):
        """ Check if items are synchronized correctly """
        # click on button
        self.main_generator.build_pricelist_item()
        product_item = self.env['product.pricelist.item'].search([
            ('item_template_id', '=', self.item.id)])[0]
        self.assertEqual(self.item.price_surcharge,
                         product_item.price_surcharge)
        self.assertEqual(self.item.min_quantity, product_item.min_quantity)
        self.assertEqual(-self.item.price_discount / 100,
                         product_item.price_discount)

    def test_synchro_after_update(self):
        """ Check if items are synchronized correctly after update """
        # click on button
        self.main_generator.build_pricelist_item()
        self.item.write({'price_discount': 33.0})
        self.main_generator.build_pricelist_item()
        product_item = self.env['product.pricelist.item'].search([
            ('item_template_id', '=', self.item.id)])[0]
        self.assertEqual(product_item.price_discount, -0.33)

    def test_copy_one2many(self):
        """ Check if we one2many field duplicate works """
        self.main_generator.write(
            {'copy_item_template': True, 'copy_product_condition': False})
        gen_copy = self.main_generator.copy()
        self.assertEqual(len(gen_copy.item_template_ids), 3)
        self.assertEqual(len(gen_copy.product_condition_ids), 0)

    def setUp(self):
        super(TestItemGenerator, self).setUp()
        self.main_generator = self.env.ref(
            'pricelist_item_generator.demo_generator')
        self.item = self.env.ref(
            'pricelist_item_generator.item_1000')
        # intialisation
        self.main_generator.activate_generator()
