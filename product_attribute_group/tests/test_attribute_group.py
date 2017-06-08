# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP / Odoo, Open Source Management Solution - module extension
#    Copyright (C) 2014- O4SB (<http://openforsmallbusiness.co.nz>).
#    Author Graeme Gellatly <g@o4sb.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests.common import TransactionCase
from openerp import exceptions


class TestAttributeGroupCase(TransactionCase):
    """
    Base Test Case provides basic setup plus range of
    helper methods for descendents.  These tests are
    tightly coupled to demo data.
    """
    def create_attribute_line(self, template, attr_group):
        attr_line_obj = self.env['product.attribute.line']
        attr_line = attr_line_obj.create({
            'attribute_id': attr_group.attribute_id.id,
            'product_tmpl_id': template.id
        })
        attr_line = self.add_attribute_group_to_line(attr_line, attr_group)

        return attr_line

    def add_attribute_group_to_line(self, attr_line, attr_group):
        attr_line.attribute_group_ids = (attr_line.attribute_group_ids +
                                         attr_group)

        attr_line._onchange_attribute_group_ids()
        attr_line._onchange_value_ids()

        attr_line.product_tmpl_id.write(
            {'attribute_line_ids': [(1, attr_line.id, {})]})
        return attr_line

    def create_value(self, vals=None):
        if vals is None:
            vals = {'name': 'Gray',
                    'attribute_id': self.color.id}
        return self.env['product.attribute.value'].create(vals)

    def add_value_to_group(self, group, value=None):
        if value is None:
            value = self.create_value()

        group.attribute_value_ids = (group.attribute_value_ids + value)
        return value

    def get_reference(self, xml_int, model, module):
        if not xml_int:
            return self.env[model]
        return self.env.ref('%s.%s_%d' % (
            module, model.replace('.', '_'), xml_int))

    def get_template(self, xml_int, model='product.product',
                     module='product_attribute_group'):
        return self.get_reference(xml_int, model, module)

    def get_attribute_group(self, xml_int, model='product.attribute.group',
                            module='product_attribute_group'):
        return self.get_reference(xml_int, model, module)

    def get_attribute_value(self, xml_int, model='product.attribute.value',
                            module='product_attribute_group'):
        return self.get_reference(xml_int, model, module)

    def setUp(self):
        super(TestAttributeGroupCase, self).setUp()
        self.attr_groups = [self.get_attribute_group(x) for x in xrange(5)]
        self.widgets = [self.get_template(x) for x in xrange(5)]
        self.color = self.env.ref('product.product_attribute_2')


class SimpleAttributeGroupCase(TestAttributeGroupCase):

    def setUp(self):
        super(SimpleAttributeGroupCase, self).setUp()

    def test01_copy_attribute_group(self):
        orig_group = self.attr_groups[1]
        self.add_value_to_group(orig_group)
        copied_group = orig_group.copy()
        self.assertEqual(copied_group.attribute_line_ids,
                         self.env['product.attribute.line'])

    def test02a_unlink_attribute_group_prohibited(self):
        self.create_attribute_line(self.widgets[1], self.attr_groups[1])
        self.attr_groups[1].write({})
        with self.assertRaises(exceptions.except_orm):
            self.attr_groups[1].unlink()

    def test02b_unlink_attribute_group_normal(self):
        attr_2_id = self.attr_groups[2].id
        self.attr_groups[2].unlink()
        self.assertEqual(self.attr_groups[0].search([('id', '=', attr_2_id)]),
                         self.attr_groups[0])

    def test04_onchange_attribute_value_ids(self):
        self.create_attribute_line(self.widgets[1], self.attr_groups[1])
        warning = self.attr_groups[1]._onchange_attribute_value_ids()
        self.assertIn('warning', warning)

        warning = self.attr_groups[2]._onchange_attribute_value_ids()
        self.assertIsNone(warning)

    def test05a_onchange_attribute_id_prohibited(self):
        self.create_attribute_line(self.widgets[1], self.attr_groups[1])
        with self.assertRaises(exceptions.except_orm):
            self.attr_groups[1]._onchange_attribute_id()

    def test05b_onchange_attribute_id(self):
        self.attr_groups[1]._onchange_attribute_id()
        self.assertEqual(self.attr_groups[1].attribute_value_ids,
                         self.env['product.attribute.value'])

    def test06_constraint_attribute_id(self):

        with self.assertRaises(exceptions.ValidationError):
            self.attr_groups[1].attribute_id = self.env.ref(
                'product.product_attribute_1')


class EnhancedAttributeGroupTestCase(TestAttributeGroupCase):

    def setUp(self):
        """
        Widget 1: single group, no manual addition
        Widget 2: single group with manual addition
        Widget 3: 2 non-overlapping group
        Widget 4: 2 overlapping groups
        :return:
        """
        super(EnhancedAttributeGroupTestCase, self).setUp()
        self.create_attribute_line(self.widgets[1], self.attr_groups[1])

        line2 = self.create_attribute_line(
            self.widgets[2], self.attr_groups[1])
        line2.value_ids = line2.value_ids + self.get_attribute_value(1)
        line2._onchange_value_ids()
        self.widgets[2].write({'attribute_line_ids': [(1, line2.id, {})]})

        line3 = self.create_attribute_line(
            self.widgets[3], self.attr_groups[1])
        self.add_attribute_group_to_line(line3, self.attr_groups[3])

        line4 = self.create_attribute_line(
            self.widgets[4], self.attr_groups[2])
        self.add_attribute_group_to_line(line4, self.attr_groups[3])

    def test03a_action_update_variants_addition(self):
        expected_counts = (0,
                           self.widgets[1].product_variant_count + 1,
                           self.widgets[2].product_variant_count + 1,
                           self.widgets[3].product_variant_count + 1,
                           self.widgets[4].product_variant_count)
        new_value = self.add_value_to_group(self.attr_groups[1])

        self.attr_groups[1].write({})
        self.attr_groups[1].action_update_variants()

        for i in range(1, 4):
            with self.subTest(i=i):
                self.assertEqual(expected_counts[i],
                                 self.widgets[i].product_variant_count)
                self.assertIn(new_value,
                              self.widgets[i].attribute_line_ids[0].value_ids)

    def test03b_action_update_variants_addition_overlap(self):
        expected_counts = (0,
                           self.widgets[1].product_variant_count,
                           self.widgets[2].product_variant_count,
                           self.widgets[3].product_variant_count + 1,
                           self.widgets[4].product_variant_count)

        self.add_value_to_group(self.attr_groups[3],
                                self.get_attribute_value(2))

        self.attr_groups[3].write({})
        self.attr_groups[3].action_update_variants()

        for i in range(1, 5):
            with self.subTest(i=i):
                self.assertEqual(expected_counts[i],
                                 self.widgets[i].product_variant_count)

    def test03c_action_update_variants_removal(self):
        expected_counts = (0,
                           self.widgets[1].product_variant_count - 1,
                           self.widgets[2].product_variant_count - 1,
                           self.widgets[3].product_variant_count - 1,
                           self.widgets[4].product_variant_count)

        deleted_value = self.get_attribute_value(3, module='product')
        self.attr_groups[1].attribute_value_ids = (
            self.attr_groups[1].attribute_value_ids - deleted_value)

        self.attr_groups[1].write({})
        self.attr_groups[1].action_update_variants()

        for i in range(1, 4):
            with self.subTest(i=i):
                self.assertEqual(expected_counts[i],
                                 self.widgets[i].product_variant_count)
                self.assertNotIn(
                    deleted_value,
                    self.widgets[i].attribute_line_ids[0].value_ids)

    def test03d_action_update_variants_removal_overlap(self):
        expected_counts = (0,
                           self.widgets[1].product_variant_count,
                           self.widgets[2].product_variant_count,
                           self.widgets[3].product_variant_count - 1,
                           self.widgets[4].product_variant_count)

        deleted_value = self.get_attribute_value(1)
        self.attr_groups[3].attribute_value_ids = (
            self.attr_groups[3].attribute_value_ids - deleted_value)

        self.attr_groups[3].write({})
        self.attr_groups[3].action_update_variants()

        for i in range(1, 4):
            with self.subTest(i=i):
                self.assertEqual(expected_counts[i],
                                 self.widgets[i].product_variant_count)

    def test07a_onchange_value_ids_normal(self):

        line = self.widgets[1].attribute_line_ids[0]
        value = self.create_value()
        line.value_ids = line.value_ids + value
        line._onchange_value_ids()

        self.assertIn(value, line.value_ids)
        self.assertIn(value, line.manually_added_value_ids)

        line.value_ids = line.value_ids - value
        line._onchange_value_ids()

        self.assertNotIn(value, line.value_ids)
        self.assertNotIn(value, line.manually_added_value_ids)

    def test07b_onchange_value_ids_abnormal(self):
        line = self.widgets[1].attribute_line_ids[0]
        auto_value = line.value_ids[0]
        value = self.create_value()
        line.value_ids = line.value_ids - auto_value + value

        warning = line._onchange_value_ids()

        self.assertIn(value, line.value_ids)
        self.assertIn(value, line.manually_added_value_ids)
        self.assertIn('warning', warning)

    def test08_onchange_attribute_group_ids(self):
        expected_count = len(self.attr_groups[3].attribute_value_ids)

        line = self.widgets[3].attribute_line_ids[0]
        line.attribute_group_ids = (line.attribute_group_ids -
                                    self.attr_groups[1])
        line._onchange_attribute_group_ids()
        self.assertEqual(len(line.value_ids), expected_count)

        line = self.widgets[4].attribute_line_ids[0]
        line.attribute_group_ids = (line.attribute_group_ids -
                                    self.attr_groups[2])
        line._onchange_attribute_group_ids()
        self.assertEqual(len(line.value_ids), expected_count)
