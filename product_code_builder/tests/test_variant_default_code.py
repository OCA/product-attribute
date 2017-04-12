# -*- coding: utf-8 -*-
#    Copyright 2017
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

from odoo.tests.common import TransactionCase
from odoo.exceptions import MissingError


class TestTemplateCreateandWrite(TransactionCase):

    def test_create_no_mask(self):
        template = self.env['product.template'].create(
            {'name': 'Variant Test',
             'attribute_line_ids': [
                 (0, 0, {'attribute_id': self.attribute1.id,
                         'value_ids': [
                             (6, 0, self.attribute1.value_ids.mapped('id'))]}),
                 (0, 0, {'attribute_id': self.attribute2.id,
                         'value_ids': [
                             (6, 0, self.attribute2.value_ids.mapped('id'))]})
             ]})
        self.assertFalse(template.reference_mask is False)

    def test_write_no_mask_no_variants(self):
        """
        Ensure that creating a template without mask does not
        create a reference mask and that when later adding lines a
        default reference mask is added
        """
        template = self.env['product.template'].create(
            {'name': 'Variant Test (no attrs)'})
        self.assertTrue(template.reference_mask is False)
        template.write({'attribute_line_ids': [
            (0, 0, {'attribute_id': self.attribute1.id,
                    'value_ids': [
                        (6, 0, self.attribute1.value_ids.mapped('id'))]}),
            (0, 0, {'attribute_id': self.attribute2.id,
                    'value_ids': [
                        (6, 0, self.attribute2.value_ids.mapped('id'))]})
        ]})
        self.assertFalse(template.reference_mask is False)

    def setUp(self):
        super(TestTemplateCreateandWrite, self).setUp()
        attr_obj = self.env['product.attribute']
        attr_value_obj = self.env['product.attribute.value']
        self.attribute1 = attr_obj.create({'name': 'Size (VDC)'})
        attr_value_obj.create({'attribute_id': self.attribute1.id,
                               'name': 'Medium',
                               'code': 'M'})
        attr_value_obj.create({'attribute_id': self.attribute1.id,
                               'name': 'Large',
                               'code': 'L'})

        self.attribute2 = attr_obj.create({'name': 'Color (VDC)'})
        attr_value_obj.create({'attribute_id': self.attribute2.id,
                               'name': 'Red'})
        attr_value_obj.create({'attribute_id': self.attribute2.id,
                               'name': 'Green'})


class TestCodeOnTemplate(TransactionCase):

    def test_invalid_mask(self):
        """Ensure a reference mask with an invalid attribute fails"""
        with self.assertRaises(MissingError):
            self.template.write({'reference_mask': 'TEST[Dummy]'})

    def test_manual_code(self):
        """Ensure a manual code set on a product is kept"""
        old_codes = self.template.product_variant_ids.mapped('default_code')
        product = self.template.product_variant_ids[0]
        product.write({'default_code': 'TESTMANUAL',
                       'manual_code': True})
        self.template.reference_mask = 'TEST[Color (VDC)][Size (VDC)]'
        new_codes = self.template.product_variant_ids.mapped('default_code')
        # Check we updated other codes
        self.assertFalse(any([n in old_codes for n in new_codes]))
        self.assertTrue(product.default_code == 'TESTMANUAL')

    def test_code_generation(self):
        """Ensure generated codes are correct"""
        product_codes = {'TESTMRe', 'TESTLRe', 'TESTMGr', 'TESTLGr'}
        # for debug check creation worked
        self.assertTrue(len(self.template.product_variant_ids) == 4)

        self.assertEqual(
            set(self.template.product_variant_ids.mapped('default_code')),
            product_codes)

    def test_default_code_creation(self):
        """
        Ensure that the automatic encoding of attributes works
        :return:
        """
        for value in self.attribute2.value_ids:
            self.assertEqual(
                value.code, value.name[:2])

    def test_writing_new_code(self):
        """Ensure changing an attribute code changes associated part code"""
        product_codes = {'TESTMX', 'TESTLX', 'TESTMY', 'TESTLY'}
        self.attribute2.value_ids[0].code = 'X'
        self.attribute2.value_ids[1].code = 'Y'
        self.assertEqual(
            set(self.template.product_variant_ids.mapped('default_code')),
            product_codes)

    def setUp(self):
        super(TestCodeOnTemplate, self).setUp()
        attr_obj = self.env['product.attribute']
        attr_value_obj = self.env['product.attribute.value']

        self.attribute1 = attr_obj.create({'name': 'Size (VDC)'})
        attr_value_obj.create({'attribute_id': self.attribute1.id,
                               'name': 'Medium',
                               'code': 'M'})
        attr_value_obj.create({'attribute_id': self.attribute1.id,
                               'name': 'Large',
                               'code': 'L'})

        self.attribute2 = attr_obj.create({'name': 'Color (VDC)'})
        attr_value_obj.create({'attribute_id': self.attribute2.id,
                               'name': 'Red'})
        attr_value_obj.create({'attribute_id': self.attribute2.id,
                               'name': 'Green'})

        self.template = self.env['product.template'].create(
            {'name': 'Variant Test',
             'reference_mask': 'TEST[Size (VDC)][Color (VDC)]',
             'attribute_line_ids': [
                 (0, 0, {'attribute_id': self.attribute1.id,
                         'value_ids': [
                             (6, 0, self.attribute1.value_ids.mapped('id'))]}),
                 (0, 0, {'attribute_id': self.attribute2.id,
                         'value_ids': [
                             (6, 0, self.attribute2.value_ids.mapped('id'))]})
             ]}
        )
