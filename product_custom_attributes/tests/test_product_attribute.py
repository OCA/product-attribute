# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   base_attribute.attributes for OpenERP                                     #
#   Copyright (C) 2015 Odoo Community Association (OCA)                       #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.tests.common import TransactionCase


class TestProductAttribute(TransactionCase):

    def create_attribute(self, vals):
        fields = self.field_model.search([
            ('name', '=', vals['name']),
            ('model_id', '=', vals['model_id']),
        ])

        if fields:
            vals['field_id'] = fields[0].id

        return self.attribute_model.create(vals)

    def setUp(self):

        super(TestProductAttribute, self).setUp()

        self.attribute_model = self.env['attribute.attribute']
        self.set_model = self.env['attribute.set']
        self.group_model = self.env['attribute.group']
        self.location_model = self.env['attribute.location']
        self.option_model = self.env['attribute.option']
        self.wizard_model = self.env['attribute.option.wizard']
        self.model_model = self.env['ir.model']
        self.field_model = self.env['ir.model.fields']
        self.product_model = self.env['product.product']

        self.model = self.env['ir.model'].search([
            ('model', '=', 'product.template')])[0]

        self.set_1 = self.set_model.create({
            'name': 'Product Set 1',
            'model_id': self.model.id,
        })

        self.set_2 = self.set_model.create({
            'name': 'Product Set 2',
            'model_id': self.model.id,
        })

        self.group_1 = self.group_model.create({
            'name': 'Product Group 1',
            'attribute_set_id': self.set_1.id,
            'model_id': self.model.id,
        })

        self.attribute_1 = self.create_attribute({
            'field_description': 'Product Attribute 1',
            'name': 'x_attribute_1',
            'attribute_type': 'char',
            'model_id': self.model.id,
        })

        self.attribute_2 = self.create_attribute({
            'field_description': 'Product Attribute 1',
            'name': 'x_attribute_2',
            'attribute_type': 'select',
            'model_id': self.model.id,
        })

        self.option_1 = self.option_model.create({
            'name': 'TEST 1',
            'attribute_id': self.attribute_2.id,
        })

        self.product = self.product_model.create({
            'name': 'Product1',
            'attribute_set_id': self.set_1.id,
        })

    def test_write_attribute_values_char(self):
        self.product.x_attribute_1 = 'abcd'
        self.assertEqual(self.product.x_attribute_1, 'abcd')

    def test_write_attribute_values_select(self):
        self.product.x_attribute_2 = self.option_1.id
        self.assertEqual(self.product.x_attribute_2, self.option_1)
