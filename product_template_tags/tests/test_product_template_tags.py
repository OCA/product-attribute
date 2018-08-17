from odoo.tests.common import TransactionCase


class TestProductTemplateTag(TransactionCase):
    pre_install = True
    post_install = True

    def test_products_count(self):
        tag = self.env['product.template.tag'].create({
            'name': 'test_tag',
        })
        product = self.env['product.template'].search([], limit=1)
        product.write({
            'tag_ids': [(6, 0, [tag.id])],
        })
        self.assertEqual(product.tag_ids[0].products_count,
                         1,
                         'Error product count does not match')
