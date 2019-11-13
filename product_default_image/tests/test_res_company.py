# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from .setup import Setup

from ..image_constants import (
    NONE,
    GLOBAL,
    CATEGORY,
    GLOBAL_CATEGORY,
)


class TestResCompany(Setup):

    def test_default_product_image(self):
        """ Test product default image correct """
        self.assertTrue(
            self.company_1.product_image,
            'Company does not correctly have default img '
            'for product.'
        )
        self.assertEquals(
            self.company_1.product_image,
            self.env['res.company']._default_product_image(),
            '_default_product_image not the same as company product image'
        )

    def test_write_target_global(self):
        """ Test imgs changed when product img target global """
        self.assertFalse(
            self.tmpl_1.image,
            'Tmpl 1 image should be False',
        )
        self.company_1.product_image_target = GLOBAL
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'Tmpl 1 image not the same as company img',
        )

    def test_write_target_none_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = GLOBAL
        self.assertNotEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should not be same as self.img_red'
        )
        self.company_1.product_image = self.img_red
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be the same as self.img_red'
        )

    def test_write_target_none_not_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = NONE
        self.company_1.product_image = self.img_red
        self.assertNotEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should not be the same as img_red'
        )

    def test_write_target_category_not_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = CATEGORY
        self.company_1.product_image = self.img_red
        self.assertNotEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should not be the same as img_red'
        )

    def test_write_target_global_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = GLOBAL
        self.company_1.product_image = self.img_red
        self.assertEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be the same as img_red'
        )

    def test_write_target_global_category_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.company_1.product_image = self.img_red
        self.assertEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be the same as img_red'
        )

    def test_write_target_global_write_not_change_image(self):
        """ Test tmpl img changed when changing company product img """
        self.company_1.product_image_target = NONE
        self.company_1.write({'product_image': self.img_red})
        self.assertNotEqual(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should not be the same as img_red'
        )

    def test_write_target_global_change_both(self):
        """ Test tmpl has correct img after writing both vals to company """
        self.company_1.write({
            'product_image_target': GLOBAL,
            'product_image': self.img_green,
        })
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.img_green,
            'tmpl_1 image should be the same as img_green'
        )

    def test_write_target_none(self):
        """ Test tmpl has no image when changing target to none """
        self.company_1.product_image_target = GLOBAL
        self.assertTrue(
            self.tmpl_1.image,
        )
        self.company_1.product_image_target = NONE
        self.assertEquals(
            self.tmpl_1.image_type,
            NONE,
        )
        self.assertFalse(
            self.tmpl_1.image,
            'Tmpl 1 image should be None'
        )

    def test_target_category(self):
        """ Test tmpl img changed to category """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = CATEGORY
        self.assertEquals(
            self.tmpl_1.image,
            self.categ_1.image,
            'Tmpl_1 image not the same as categ_1 img'
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CATEGORY,
        )

    def test_target_global_category(self):
        """ Test tmpls correct images if target global_category """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'Tmpl_1 image not the same as img_red'
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CATEGORY,
        )
        self.assertEquals(
            self.tmpl_2.image,
            self.company_1.product_image,
            'tmpl_2 image not company product image'
        )
        self.assertEquals(
            self.tmpl_2.image_type,
            GLOBAL,
        )

    def test_change_image_only_global(self):
        """ Test only global imgs change when change company product_image """
        self.company_1.product_image_target = GLOBAL
        self.tmpl_1.write({
            'image': self.img_red,
            'image_type': GLOBAL,
        })
        self.company_1.product_image = self.img_blue
        self.assertEquals(
            self.img_blue,
            self.tmpl_1.image,
            'Tmpl_1 image should be the same as self.img_blue'
        )
