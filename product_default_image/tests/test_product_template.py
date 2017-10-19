# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import patch

from .setup import Setup

from ..image_constants import (
    NONE,
    GLOBAL,
    CATEGORY,
    GLOBAL_CATEGORY,
    CUSTOM,
)

MOCK_DEFAULT_GET = 'odoo.addons.product.models.product_template.'\
                   'ProductTemplate.default_get'


class TestProductTemplate(Setup):

    @patch(MOCK_DEFAULT_GET)
    def test_default_get_category(self, default_categ):
        """ Test default_get returns categs image """
        default_categ.return_value = {'categ_id': self.categ_1.id}
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = CATEGORY
        vals = self.tmpl_mod.default_get(vals={})
        self.assertEquals(
            vals['image'],
            self.img_red,
            "vals['image'] should be the same as img_red",
        )
        self.assertEquals(
            vals.get('image_type'),
            CATEGORY,
            'image_type should be default_category',
        )

    @patch(MOCK_DEFAULT_GET)
    def test_default_get_global_category_with_image(self, default_categ):
        """ Test image is categs image """
        default_categ.return_value = {'categ_id': self.categ_1.id}
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = GLOBAL_CATEGORY
        vals = self.tmpl_mod.default_get(vals={})
        self.assertEquals(
            vals['image'],
            self.img_red,
            "vals['image'] should be the same as img_red",
        )
        self.assertEquals(
            vals.get('image_type'),
            CATEGORY,
            'image_type should be default_category',
        )

    def test_default_get_global(self):
        """ Test image set to global product image """
        self.company_1.product_image_target = GLOBAL
        vals = self.tmpl_mod.default_get(vals={})
        self.assertEquals(
            vals['image'],
            self.company_1.product_image,
            "vals['image'] should be the same as company product_image",
        )
        self.assertEquals(
            vals.get('image_type'),
            GLOBAL,
            'image_type should be default_global',
        )

    def test_default_resize_images(self):
        """ Test images properly resized """
        self.company_1.product_image_target = GLOBAL
        vals = self.tmpl_mod.default_get(vals={})
        self.assertTrue(
            all([
                vals['image'],
                vals['image_medium'],
                vals['image_small'],
            ])
        )

    @patch(MOCK_DEFAULT_GET)
    def test_default_get_global_category_none(self, default_categ):
        """ Test image set to global product image """
        default_categ.return_value = {'categ_id': self.categ_1.id}
        self.categ_1.image = None
        self.company_1.product_image_target = GLOBAL_CATEGORY
        vals = self.tmpl_mod.default_get(vals={})
        self.assertEquals(
            vals['image'],
            self.company_1.product_image,
            "vals['image'] should be the same as company product_image",
        )
        self.assertEquals(
            vals.get('image_type'),
            GLOBAL,
            'image_type should be default_global',
        )

    def test_search_templates_change_images_none(self):
        """ Test returns no templates if not valid search """
        self.assertFalse(
            self.tmpl_mod._search_templates_change_images(
                from_types=['test'],
                to_type=['test'],
            )
        )

    def test_search_templates_change_images_wrong_from_types(self):
        """ Test raise TypeError if from_types not list """
        with self.assertRaises(TypeError):
            self.tmpl_mod._search_templates_change_images(
                from_types='test',
                to_type='test',
            )

    def test_search_templates_change_images_wrong_add_domain(self):
        """ Test raise TypeError if add_domain not list """
        with self.assertRaises(TypeError):
            self.tmpl_mod._search_templates_change_images(
                from_types=['test'],
                to_type='test',
                add_domain='test',
            )

    def test_write_custom_image(self):
        """ Test write sets image_type to custom properly """
        self.tmpl_1.write({
            'image': self.img_red,
        })
        self.assertEquals(
            self.tmpl_1.image_type,
            CUSTOM,
        )

    def test_write_flexible(self):
        """ Test write does not set custom if image_type defined """
        self.tmpl_1.write({
            'image': self.img_red,
            'image_type': GLOBAL,
        })
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )

    def test_write_none(self):
        """ Test write overrides image_type to none if None """
        self.tmpl_1.write({
            'image': self.img_red,
            'image_type': GLOBAL,
        })
        self.tmpl_mod._search_templates_change_images(
            from_types=[GLOBAL],
            to_type=CATEGORY,
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            NONE,
        )

    def test_apply_default_image_auto_change_image(self):
        """ Test auto_change_image set to True if method called """
        self.tmpl_1.auto_change_image = False
        self.tmpl_1.apply_default_image()
        self.assertTrue(
            self.tmpl_1.auto_change_image,
        )

    def test_apply_default_image_none(self):
        """ Test overrides custom image to none """
        self.company_1.product_image_target = NONE
        self.tmpl_1.image = self.img_red
        self.tmpl_1.apply_default_image()
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None',
        )

    def test_apply_default_image_global(self):
        """ Test overrides custom image with global image """
        self.company_1.product_image_target = GLOBAL
        self.tmpl_1.image = self.img_red
        self.tmpl_1.apply_default_image()
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'tmpl_1 image should be equal to company product image',
        )

    def test_apply_default_image_category(self):
        """ Test overrides custom image with category image """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = CATEGORY
        self.tmpl_1.image = self.img_green
        self.tmpl_1.apply_default_image()
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 image should be equal to img_red',
        )

    def test_apply_default_image_global_category_image(self):
        """ Test overrides custom image with category image """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.tmpl_1.image = self.img_green
        self.tmpl_1.apply_default_image()
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 image should be equal to img_red',
        )

    def test_apply_default_image_global_category_none(self):
        """ Test overrides custom image with category image """
        self.categ_1.image = None
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.tmpl_1.image = self.img_green
        self.tmpl_1.apply_default_image()
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'tmpl_1 image should be equal to company product image',
        )

    def test_onchange_categ_id_not_valid_target(self):
        """ Test no img changes if target incorrect """
        self.company_1.product_image_target = NONE
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None after changing '
            'target to none'
        )
        self.categ_2.image = self.img_red
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None'
        )

    def test_onchange_categ_id_auto_change_image_false(self):
        """ Test no img changes if auto_change_image is False """
        self.company_1.product_image_target = CATEGORY
        self.categ_2.image = self.img_red
        self.tmpl_1.auto_change_image = False
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None'
        )

    def test_onchange_categ_id_auto_change_image_custom(self):
        """ Test no img changes if image is custom """
        self.company_1.product_image_target = CATEGORY
        self.categ_2.image = self.img_red
        self.tmpl_1.image = self.img_green
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertEquals(
            self.tmpl_1.image,
            self.img_green,
            'tmpl_1 image should be img_green'
        )

    def test_onchange_categ_id_all_images_changed(self):
        """ Test all image fields changed with onchange """
        self.company_1.product_image_target = CATEGORY
        self.categ_2.image = self.img_red
        self.tmpl_1.categ_id = self.categ_2
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None'
        )
        self.tmpl_1._onchange_categ_id()
        self.assertTrue(
            all([
                self.tmpl_1.image,
                self.tmpl_1.image_medium,
                self.tmpl_1.image_small,
            ]),
        )

    def test_onchange_categ_id_category(self):
        """ Test successfully changes to new categ img """
        self.company_1.product_image_target = CATEGORY
        self.categ_2.image = self.img_red
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertEquals(
            self.tmpl_1.image[:11],
            self.img_red[:11],
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CATEGORY,
        )

    def test_onchange_categ_id_global_category_with_image(self):
        """ Test successfully changes to new categ img if global_category """
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.categ_2.image = self.img_red
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertEquals(
            self.tmpl_1.image[:11],
            self.img_red[:11],
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CATEGORY,
        )

    def test_onchange_categ_id_global_category_none(self):
        """" Test changed to company product image if no categ image """
        self.categ_1.image = self.img_red
        self.company_1.product_image_target = GLOBAL_CATEGORY
        self.tmpl_1.categ_id = self.categ_2
        self.tmpl_1._onchange_categ_id()
        self.assertEquals(
            self.tmpl_1.image[:11],
            self.company_1.product_image[:11],
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )

    def test_search_templates_change_images_wrong_company(self):
        """ Test image not changed if tmpl belongs to wrong company """
        self.tmpl_1.company_id = self.env.ref('base.main_company')
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=GLOBAL,
        )
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None',
        )

    def test_search_templates_change_images_auto_change_image_false(self):
        """ Test image not changed if tmpl belongs to wrong company """
        self.tmpl_1.auto_change_image = False
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=GLOBAL,
        )
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 image should be None',
        )

    def test_search_templates_change_images_custom_img(self):
        """ Test images changes to custom if specified """
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=CUSTOM,
            to_img_bg=self.img_red,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be same as img_red',
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CUSTOM,
        )

    def test_search_templates_change_images_to_img_bg_override(self):
        """ Test default_global image overrided if to_img_bg specified """
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=GLOBAL,
            to_img_bg=self.img_red,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be same as img_red',
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )

    def test_search_templates_change_images_no_img(self):
        """ Test images changes to no image if specified """
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=GLOBAL,
        )
        self.assertTrue(
            self.tmpl_1.image,
            'tmpl_1 should have an image',
        )
        self.tmpl_mod._search_templates_change_images(
            from_types=[GLOBAL],
            to_type=NONE,
        )
        self.assertFalse(
            self.tmpl_1.image,
            'tmpl_1 img should be None',
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            NONE,
        )

    def test_search_templates_change_images_different_categs(self):
        """ Test tmpls set to different categ images properly """
        self.categ_1.image = self.img_red
        self.categ_2.image = self.img_green
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=CATEGORY,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.img_red,
            'tmpl_1 img should be same as img_red',
        )
        self.assertEquals(
            self.tmpl_2.image,
            self.img_green,
            'tmpl_2 img should be same as img_green',
        )
        self.assertEquals(
            [self.tmpl_1.image_type, self.tmpl_2.image_type],
            [CATEGORY, CATEGORY]
        )

    def test_search_templates_change_images_to_global(self):
        """ Test tmpls set to global image """
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE],
            to_type=GLOBAL,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'tmpl_1 image should be same as company product_image',
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )

    def test_search_templates_change_images_multiple_from_types(self):
        """" Test products of multiple types set to to_type """
        self.tmpl_2.write({
            'image': self.img_red,
            'image_type': CATEGORY,
        })
        self.tmpl_mod._search_templates_change_images(
            from_types=[NONE, CATEGORY],
            to_type=GLOBAL,
        )
        self.assertEquals(
            self.tmpl_1.image,
            self.company_1.product_image,
            'tmpl_1 should be same as company product image',
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            GLOBAL,
        )
        self.assertEquals(
            self.tmpl_2.image,
            self.company_1.product_image,
            'tmpl_2 should be same as company product image',
        )
        self.assertEquals(
            self.tmpl_2.image_type,
            GLOBAL,
        )

    def test_change_template_image_wrong_to_type(self):
        """ Test to_type arg not in accepted vals """
        with self.assertRaises(ValueError):
            self.tmpl_1._change_template_image(
                to_type=GLOBAL_CATEGORY,
            )

    def test_change_template_image_to_type_custom_no_to_img_bg(self):
        """ Test raise error if to_type custom and no to_img_bg """
        with self.assertRaises(ValueError):
            self.tmpl_1._change_template_image(
                to_type=CUSTOM,
            )

    def test_change_template_image_to_type_none_to_img_bg(self):
        """ Test raise error if to_type none and to_img_bg """
        with self.assertRaises(ValueError):
            self.tmpl_1._change_template_image(
                to_type=NONE,
                to_img_bg=self.img_red,
            )

    def test_change_template_image_false_none(self):
        """ Test change to_type to None if img False and to_type not None. """
        self.tmpl_1.write({
            'image': self.img_red,
            'image_type': CATEGORY,
        })
        self.assertTrue(
            self.tmpl_1.image,
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            CATEGORY,
        )
        self.tmpl_1._change_template_image(
            to_type=CATEGORY,
            to_img_bg=False,
        )
        self.assertEquals(
            self.tmpl_1.image_type,
            NONE,
        )
        self.assertFalse(
            self.tmpl_1.image,
        )
