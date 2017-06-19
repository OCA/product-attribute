# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from .test_setup import TestSetup
from ..image_constants import TYPES, TARGETS


class TestAbstractProductImage(TestSetup):

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
            all(res),
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
            all(res),
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
        )

    def test_get_images_all(self):
        """ Test returns all images """
        self.tmpl_1.image = self.img_red
        self.assertTrue(
            all(self.tmpl_1._get_images()),
        )

    def test_get_images_correct_first_key(self):
        """ Test first image in return val is image field """
        self.tmpl_1.image = self.img_red
        self.assertEquals(
            self.tmpl_1._get_images()[0],
            self.img_red,
        )

    def test_get_images_image_none(self):
        """ Test returns no images """
        self.assertFalse(
            any(self.tmpl_1._get_images()),
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
        )

    def test_target_match_any_single(self):
        """ Test returns True if supplied by single valid int """
        self.assertTrue(
            self.abs_mod._target_match_any(TARGETS[1], 1)
        )

    def test_target_match_any_multiple(self):
        """ Test returns True if supplied with tuple """
        self.assertTrue(
            self.abs_mod._target_match_any(TARGETS[3], (1, 3))
        )

    def test_target_match_any_invalid_keys(self):
        """ Test returns True if given tuple of valid + invalid vals """
        self.assertTrue(
            self.abs_mod._target_match_any(TARGETS[3], (200, 3))
        )

    def test_target_match_any_not_present_single(self):
        """ Test returns False if not matched to single int """
        self.assertFalse(
            self.abs_mod._target_match_any(TARGETS[3], 2)
        )

    def test_target_match_any_not_present_multiple(self):
        """ Test returns False if not matched to any in tuple """
        self.assertFalse(
            self.abs_mod._target_match_any(TARGETS[3], (1, 2))
        )

    def test_target_match_any_not_invalid_keys(self):
        """ Test returns False if not matched to any in tuple """
        self.assertFalse(
            self.abs_mod._target_match_any(TARGETS[3], (200, 300))
        )

    def test_type_match_any_single(self):
        """ Test returns True if supplied by single valid int """
        self.assertTrue(
            self.abs_mod._type_match_any(TYPES[0], 0)
        )

    def test_type_match_any_multiple(self):
        """ Test returns True if supplied with tuple """
        self.assertTrue(
            self.abs_mod._type_match_any(TYPES[0], (0, 3))
        )
