# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProductRestrictedType(TransactionCase):

    def setUp(self):
        super(TestProductRestrictedType, self).setUp()
        self.product_product = self.env['product.product']
        self.product_category = self.env['product.category']

        self.product_types = self.env['product.template']._fields[
            'type'].selection

        self.categ_test = self.product_category.create({
            'name': 'Test Category 1',
            'restricted_product_type': self.product_types[0][0],
        })
        self.categ_test2 = self.product_category.create({
            'name': 'Test Category 2',
        })
        self.product_test = self.product_product.create({
            'name': "Test Product 1",
            'type': self.product_types[0][0],
            'categ_id': self.categ_test.id,
        })
        self.product_product.create({
            'name': "Test Product 2",
            'type': self.product_types[1][0],
            'categ_id': self.categ_test2.id,
        })

    def test_product_different_type(self):
        """User tries to change product type to a different type than
        company restricted product type"""
        with self.assertRaises(ValidationError):
            self.product_test.write({
                'type': self.product_types[1][0],
            })
        with self.assertRaises(ValidationError):
            self.product_product.create({
                'name': "Test Product 3",
                'type': self.product_types[1][0],
                'categ_id': self.categ_test.id,
            })

    def test_category_different_type(self):
        """User tries to change category restricted type but there are
        products with already defined (different) type"""
        with self.assertRaises(ValidationError):
            self.categ_test.write({
                'restricted_product_type': self.product_types[1][0],
            })
