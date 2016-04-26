# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from openerp.tests import common


class TestProductMultiImage(common.TransactionCase):
    def setUp(self):
        super(TestProductMultiImage, self).setUp()
        self.transparent_image = (  # 1x1 Transparent GIF
            "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
        self.grey_image = (  # 1x1 Grey GIF
            'R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw ==')
        self.black_image = (  # 1x1 Black GIF
            "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=")
        self.attribute = self.env['product.attribute'].create({
            'name': 'Test attribute',
        })
        self.value_1 = self.env['product.attribute.value'].create({
            'name': "Test value 1",
            'attribute_id': self.attribute.id,
        })
        self.value_2 = self.env['product.attribute.value'].create({
            'name': "Test value 2",
            'attribute_id': self.attribute.id,
        })
        self.product_template = self.env['product.template'].create({
            'name': "Test product",
            'attribute_line_ids': [
                (0, 0, {
                    'attribute_id': self.attribute.id,
                    'value_ids': [(6, 0, (self.value_1 + self.value_2).ids)],
                })],
            'image_ids': [(0, 0, {
                'storage': 'db',
                'name': 'Image 1',
                'file_db_store': self.transparent_image,
                'owner_model': 'product.template',
            }), (0, 0, {
                'storage': 'db',
                'name': 'Image 2',
                'file_db_store': self.black_image,
                'owner_model': 'product.template',
            })],
        })
        self.product_1 = self.product_template.product_variant_ids[0]
        self.product_2 = self.product_template.product_variant_ids[1]

    def test_all_images(self):
        self.assertEqual(len(self.product_template.image_ids), 2)
        self.assertEqual(len(self.product_1.image_ids), 2)
        self.assertEqual(len(self.product_2.image_ids), 2)

    def test_restrict_one_image(self):
        self.product_template.image_ids[0].product_variant_ids = [
            (6, 0, self.product_1.ids)]
        self.assertEqual(len(self.product_1.image_ids), 2)
        self.assertEqual(len(self.product_2.image_ids), 1)
        self.assertEqual(self.product_1.image, self.transparent_image)
        self.assertEqual(self.product_2.image, self.black_image)

    def test_add_image_variant(self):
        self.product_1.image_ids = [
            (0, 0, {'storage': 'db',
                    'file_db_store': self.grey_image})]
        self.product_template.refresh()
        self.assertEqual(len(self.product_template.image_ids), 3)
        self.assertEqual(
            self.product_template.image_ids[-1].product_variant_ids,
            self.product_1)

    def test_remove_image_variant(self):
        self.product_1.image_ids = [(3, self.product_1.image_ids[0].id)]
        self.product_template.refresh()
        self.assertEqual(len(self.product_template.image_ids), 2)
        self.assertEqual(
            self.product_template.image_ids[0].product_variant_ids,
            self.product_2)

    def test_remove_image_all_variants(self):
        self.product_1.image_ids = [(3, self.product_1.image_ids[0].id)]
        self.product_2.image_ids = [(3, self.product_2.image_ids[0].id)]
        self.product_template.refresh()
        self.assertEqual(len(self.product_template.image_ids), 1)

    def test_edit_image_variant(self):
        text = 'Test name changed'
        self.product_1.image_ids[0].name = text
        self.product_template.refresh()
        self.assertEqual(self.product_template.image_ids[0].name, text)

    def test_edit_main_image(self):
        self.product_1.image = self.grey_image
        self.assertEqual(
            self.product_1.image_ids[0].image_main, self.grey_image)
        self.assertEqual(
            self.product_template.image_ids[0].image_main, self.grey_image)

    def test_remove_main_image(self):
        self.product_1.image = False
        self.assertEqual(len(self.product_1.image_ids), 1)
        self.assertEqual(
            self.product_template.image_ids[0].product_variant_ids,
            self.product_2)

    def test_create_variant_afterwards(self):
        """Create a template, assign an image, and then create the variant.
        Check that the images are not lost.
        """
        template = self.env['product.template'].create({
            'name': 'Test 2',
            'image_ids': [(0, 0, {
                'storage': 'db',
                'name': 'Image 1',
                'file_db_store': self.transparent_image,
                'owner_model': 'product.template',
            })],
        })
        self.assertEqual(len(template.image_ids), 1)
        template.write({
            'attribute_line_ids': [
                (0, 0, {
                    'attribute_id': self.attribute.id,
                    'value_ids': [(6, 0, (self.value_1 + self.value_2).ids)],
                })],
        })
        self.assertEqual(len(template.image_ids), 1)
        self.assertEqual(len(template.product_variant_ids[0].image_ids), 1)

    def test_remove_variant_with_image(self):
        self.product_template.image_ids[0].product_variant_ids = [
            (6, 0, self.product_1.ids)]
        self.product_1.unlink()
        self.assertEqual(len(self.product_template.image_ids), 1)
