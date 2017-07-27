# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from .setup import Setup

from ..image_constants import (
    NONE,
    CATEGORY,
    GLOBAL_CATEGORY,
)


class TestProductCategory(Setup):

    def test_categ_write_imgs_same(self):
        """ Ensure test imgs and img in categ same after write """
        self.categ_1.write({
            'image': self.img_red,
        })
        self.assertEquals(
            self.categ_1.image,
            self.img_red,
            'categ_1 img not same as img_red'
        )

    def test_create(self):
        """ Test images resized on create """
        test_categ = self.env['product.category'].create({
            'name': 'Categ',
            'image': self.img_red,
        })
        self.assertTrue(
            all([
                test_categ.image,
                test_categ.image_medium,
                test_categ.image_small,
            ])
        )

    def test_write_resize_images(self):
        """ Test images resized on write """
        self.assertFalse(
            all([
                self.categ_1.image,
                self.categ_1.image_medium,
                self.categ_1.image_small,
            ])
        )
        self.categ_1.write({
            'image': self.img_red,
        })
        self.assertTrue(
            all([
                self.categ_1.image,
                self.categ_1.image_medium,
                self.categ_1.image_small,
            ])
        )

    def test_write_target_not_accepted(self):
        """ Test no change to tmpl image if target not categ """
        self.company_1.product_image_target = NONE
        self.categ_1.write({
            'image': self.img_red,
        })
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 img should be None',
        )

    def test_write_category_default_category(self):
        """ Test both test tmpl imgs changed """
        self.company_1.product_image_target = CATEGORY
        self.tmpl_1.image_type = CATEGORY
        self.categ_1.write({
            'image': self.img_red,
        })
        self.assertEquals(
            self.categ_1,
            self.tmpl_1.categ_id,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
        )

    def test_write_global_category_global(self):
        """ Test both test tmpl imgs changed """
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'Tmpl img and company product_img not the same',
        )
        self.categ_1.write({
            'image': self.img_red,
        })
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 image not same as img_red'
        )

    def test_write_none_category(self):
        """ Test tmpl img none if categ img deleted """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = CATEGORY
        self.assertTrue(
            self.tmpl_1.image,
        )
        self.categ_1.image = None
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 img should be None'
        )

    def test_write_none_global_category(self):
        """ Test tmp img change to global img if categ img deleted """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.assertTrue(
            self.tmpl_1.image,
        )
        self.categ_1.image = None
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'tmpl_1 img should be same as company_1 product image',
        )

    def test_write_no_imgs_present(self):
        """ Test write is successful even if no imgs present """
        self.company_1.product_image_target = CATEGORY
        self.categ_1.write({
            'name': 'Test',
        })
        self.assertEquals(
            self.categ_1.name,
            'Test',
        )
