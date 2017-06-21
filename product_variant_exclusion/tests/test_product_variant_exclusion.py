# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestProductVariantExclusion(TransactionCase):

    def setUp(self):
        super(TestProductVariantExclusion, self).setUp()
        sizes = [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
        colours = ['Green', 'Black', 'Blue', 'Yellow']
        genders = ['Women', 'Men']

        ProductAttribute = self.env['product.attribute']

        self.attribute_size = ProductAttribute.create({
            'name': 'size',
            'value_ids': [(0, False, {'name': s}) for s in sizes],
        })
        self.attribute_colour = ProductAttribute.create({
            'name': 'Colour',
            'value_ids': [(0, False, {'name': c}) for c in colours],
        })
        self.attribute_gender = ProductAttribute.create({
            'name': 'Gender',
            'value_ids': [(0, False, {'name': g}) for g in genders],
        })

    def test_create_product_template(self):

        ProductTemplate = self.env['product.template']

        self.women_value = self.env['product.attribute.value'].search([
            ('name', '=', 'Women')])

        self.product_template = ProductTemplate.create({
            'name': 'Test shoes',
            'type': 'consu',
            'categ_id': self.env.ref('product.product_category_all').id,
            'attribute_line_ids': [(0, False, {
                'attribute_id': self.attribute_size.id,
                'value_ids': [(6, False, self.attribute_size.value_ids.ids)],
            }), (0, False, {
                'attribute_id': self.attribute_colour.id,
                'value_ids': [(6, False, self.attribute_colour.value_ids.ids)],
            }), (0, False, {
                'attribute_id': self.attribute_gender.id,
                'value_ids': [(6, False, self.attribute_gender.value_ids.ids)],
            })],
            'variant_exclusion_ids': [(0, False, {
                'attribute_value_ids': [(6, False, [v.id,
                                                    self.women_value.id])]})
                                      for v in self.attribute_size.value_ids
                                      if int(v.name) > 40],
        })
        self.assertEqual(self.product_template.product_variant_count, 92)
