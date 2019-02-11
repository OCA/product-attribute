from odoo.tests import common


class TestProductTags(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env.ref('product.product_product_4')
        self.product_tag = self.env['product.template.tag'].create(
            {'name': 'Test Tag'}
        )

    def test_product_count(self):
        error_msg = 'Product Count does not match. Expected {}, got {}'

        product_count = self.product_tag.products_count
        self.assertEqual(product_count, 0, error_msg.format(0, product_count))

        self.product.write({'tag_ids': [(4, self.product_tag.id)]})
        product_count = self.product_tag.products_count
        self.assertEqual(product_count, 1, error_msg.format(1, product_count))
