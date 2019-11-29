from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductAttribute(TransactionCase):

    def setUp(self):
        super(TestProductAttribute, self).setUp()
        self.attribute_select_id = self.env['product.attribute'].create({
            'name': 'Test Attribute',
            'attr_type': 'select',
        })
        self.attribute_range_id = self.env['product.attribute'].create({
            'name': 'Test Attribute',
            'attr_type': 'range',
        })

    def test_product_attribute_value_type_select(self):
        self.attribute_value = self.env['product.attribute.value'].create({
            'name': 'Test Select Value',
            'attribute_id': self.attribute_select_id.id,
            'min_range': 5.0,
            'max_range': 10.0
        })
        self.assertTrue(self.attribute_value)

    def test_product_attribute_value_type_range(self):
        with self.assertRaises(ValidationError):
            self.env['product.attribute.value'].create({
                'name': 'Test',
                'attribute_id': self.attribute_range_id.id,
                'min_range': 12.0,
                'max_range': 10.0
            })
