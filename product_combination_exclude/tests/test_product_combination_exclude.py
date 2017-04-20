# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductCombinationExclude(TransactionCase):

    def test_button_generate_exclusions(self):
        base_count = self.product3.product_variant_count

        self.matrix1.button_generate_exclusions()
        self.assertEqual(len(self.matrix1.exclusion_line_ids), 2)

        self.matrix2.button_generate_exclusions()
        self.assertEqual(len(self.matrix2.exclusion_line_ids), 1)

        self.matrix2.button_update_products()
        self.assertEqual(self.product1.product_variant_count, base_count - 3)
        self.assertEqual(self.product2.product_variant_count, base_count - 1)
        self.assertEqual(self.product3.product_variant_count, base_count)

        # Misc check to prove that at least one excluded variant
        # is not available
        large_green_tshirts = self.env['product.product'].search(
            [('attribute_value_ids', 'in', [self.large.id]),
             ('attribute_value_ids', 'in', [self.green.id])]
        )
        self.assertEqual(len(large_green_tshirts), 1)
        self.assertEqual(large_green_tshirts.product_tmpl_id.id,
                         self.product3.id)

    def test_new_variant_creation(self):
        # Add purple to the exclusions matrix so it now has
        # 3 possible exclusions
        self.matrix1.attribute_value_ids |= self.purple
        self.matrix1.button_generate_exclusions()

        self.attr_line_2.value_ids |= self.purple
        self.product1.create_variant_ids()

        # Check we didn't create Medium Purple T-Shirts but still
        # Created purple and medium T-Shirts
        self.assertFalse(self.product_obj.search([
            ('attribute_value_ids', 'in', [self.purple.id]),
            ('attribute_value_ids', 'in', [self.medium.id])
        ]))
        self.assertTrue(self.product_obj.search([
            ('attribute_value_ids', 'in', [self.purple.id])
        ]))
        self.assertTrue(self.product_obj.search([
            ('attribute_value_ids', 'in', [self.medium.id])
        ]))

    def setUp(self):
        super(TestProductCombinationExclude, self).setUp()

        #  This matrix says we cannot have Green and Black T-Shirts
        #  in medium size
        self.matrix1 = self.browse_ref(
            'product_combination_exclude.exclude_matrix_test_1')

        #  This matrix says we cannot have Green T-Shirts
        #  in large size
        self.matrix2 = self.browse_ref(
            'product_combination_exclude.exclude_matrix_test_2')

        #  all 3 products have the same attribute values, but different
        #  exclusion matrices
        self.product1 = self.browse_ref(
            'product_combination_exclude.product_exclude_test_1')
        self.product2 = self.browse_ref(
            'product_combination_exclude.product_exclude_test_2')
        self.product3 = self.browse_ref(
            'product_combination_exclude.product_exclude_test_3')
        self.product3.create_variant_ids()
        self.product_obj = self.env['product.product']

        self.green = self.browse_ref(
            'product_combination_exclude.product_attribute_value_7')
        self.purple = self.browse_ref(
            'product_combination_exclude.product_attribute_value_9')
        self.medium = self.browse_ref(
            'product_combination_exclude.product_attribute_value_2')
        self.large = self.browse_ref(
            'product_combination_exclude.product_attribute_value_3')

        self.attr_line_2 = self.browse_ref(
            'product_combination_exclude.product_attribute_line_2')
