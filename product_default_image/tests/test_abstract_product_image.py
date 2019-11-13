# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from .setup import Setup


class TestAbstractProductImage(Setup):

    def test_vals_get_images_all(self):
        """ Test returns all images """
        vals = {
            'image': self.img_red,
            'image_medium': self.img_red,
            'image_small': self.img_red,
        }
        res = self.abs_mod._vals_get_images(vals)
        self.assertEquals(
            len(res),
            3,
        )
        self.assertTrue(
            res,
        )

    def test_vals_get_images_correct_first_key(self):
        """ Test first image in return val is image field """
        vals = {
            'image': self.img_green,
            'image_medium': self.img_red,
            'image_small': self.img_red,
        }
        self.assertEquals(
            self.abs_mod._vals_get_images(vals)[0],
            self.img_green,
            'First img should be same as self.img_green'
        )

    def test_vals_get_images_image(self):
        """ Test returns image key """
        vals = {
            'image': self.img_red,
        }
        res = self.abs_mod._vals_get_images(vals)
        self.assertEquals(
            len(res),
            1,
        )
        self.assertTrue(
            res,
        )

    def test_vals_get_images_image_none_key(self):
        """ Test returns 2 images """
        vals = {
            'image': self.img_red,
            'image_medium': None,
        }
        self.assertEquals(
            len(self.abs_mod._vals_get_images(vals)),
            2,
        )

    def test_vals_get_images_image_false_filter_false(self):
        """ Test returns no images """
        vals = {
            'image': self.img_red,
            'image_medium': None,
        }
        self.assertEquals(
            len(self.abs_mod._vals_get_images(vals)),
            2,
        )

    def test_vals_get_images_image_false_filter_true(self):
        """ Test returns no images """
        vals = {
            'image': self.img_red,
            'image_medium': None,
        }
        self.assertEquals(
            len(self.abs_mod._vals_get_images(vals, false_filter=True)),
            1,
        )

    def test_vals_get_images_image_none(self):
        """ Test returns no images """
        vals = {
            'test': 'test',
        }
        self.assertEquals(
            len(self.abs_mod._vals_get_images(vals)),
            0,
        )

    def test_vals_get_images_all_update_keys(self):
        """ Test returns 1 image even though all images supplied """
        vals = {
            'image': self.img_green,
            'image_medium': self.img_red,
            'image_small': self.img_red,
        }
        res = self.abs_mod._vals_get_images(
            vals=vals,
            img_keys='image',
        )
        self.assertEquals(
            len(res),
            1,
        )
        self.assertEquals(
            res[0],
            self.img_green,
            'First image should be same as img_green'
        )

    def test_get_images_all(self):
        """ Test returns all images """
        self.tmpl_1.image = self.img_red
        self.assertTrue(
            self.tmpl_1._get_images(),
        )

    def test_get_images_correct_first_key(self):
        """ Test first image in return val is image field """
        self.tmpl_1.image = self.img_red
        self.assertEquals(
            self.tmpl_1._get_images()[0],
            self.img_red,
            'First image should be same as img_red'
        )

    def test_get_images_image_none(self):
        """ Test returns empty list """
        self.assertFalse(self.tmpl_1._get_images(false_filter=True))

    def test_get_images_none(self):
        """ Test returns no images """
        self.assertEquals(
            self.tmpl_1._get_images(),
            [False] * 3,
            'Image values should all be False'
        )

    def test_get_images_all_update_keys(self):
        """ Test returns 1 image even though all images supplied """
        self.tmpl_1.image = self.img_red
        res = self.tmpl_1._get_images(
            img_keys='image',
        )
        self.assertEquals(
            len(res),
            1,
        )
        self.assertEquals(
            res[0],
            self.img_red,
            'First image should be img_red.'
        )
