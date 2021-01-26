# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import ABCClassificationLevelCase


class TestProduct(ABCClassificationLevelCase):
    @classmethod
    def setUpClass(cls):
        super(TestProduct, cls).setUpClass()

    def test_00(self):
        """
        Data:
            A product template with one variant.
        Test Case:
            1. Associate a classification profile to the template
            2. Unset the classifiation profile
        Expected:
            1. The classification profile is also associated to the variant
            2. The classification profile no more associated to the variant
        """
        self.assertFalse(self.product_template.abc_classification_profile_ids)
        self.assertFalse(self.product_product.abc_classification_profile_ids)
        # 1
        self.product_template.abc_classification_profile_ids = (
            self.classification_profile
        )
        self.assertEqual(
            self.product_product.abc_classification_profile_ids,
            self.classification_profile,
        )
        # 2
        self.product_template.abc_classification_profile_ids = False
        self.assertFalse(self.product_product.abc_classification_profile_ids)

    def test_01(self):
        """
        Data:
            A product template with two variants (without profiles).
        Test Case:
            1. Associate a classification profile to the template
        Expected:
            The classification profile is not associated to the variant
        """
        self._create_variant(self.size_attr_value_m)
        variants = self.product_template.product_variant_ids
        self.assertEqual(len(variants), 2)
        self.assertFalse(variants.mapped("abc_classification_profile_ids"))
        self.product_template.abc_classification_profile_ids = (
            self.classification_profile
        )
        self.assertFalse(variants.mapped("abc_classification_profile_ids"))

    def test_02(self):
        """
        Data:
            A product template with one variant
        Test Case:
            1 Associate a product level to the variant
            2 unlink the level
        Expected result:
            1 The product level is also associated to the template
            2 No more level associated to the template
        """
        product_level = self.ProductLevel.create(
            {
                "product_id": self.product_product.id,
                "computed_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id,
            }
        )
        self.assertEqual(
            self.product_product.abc_classification_product_level_ids,
            product_level,
        )
        self.assertEqual(
            self.product_template.abc_classification_product_level_ids,
            product_level,
        )
        product_level.unlink()

        self.assertFalse(
            self.product_product.abc_classification_product_level_ids
        )
        self.assertFalse(
            self.product_template.abc_classification_product_level_ids
        )

    def test_03(self):
        """
        Data:
            A product template with two variants
        Test Case:
            Associate a product level to one variant
        Expected result:
            The product level is not associated to the template
        """
        new_variant = self._create_variant(self.size_attr_value_m)
        variants = self.product_template.product_variant_ids
        self.assertEqual(len(variants), 2)
        product_level = self.ProductLevel.create(
            {
                "product_id": new_variant.id,
                "computed_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id,
            }
        )
        self.assertEqual(
            new_variant.abc_classification_product_level_ids, product_level,
        )
        self.assertFalse(
            self.product_template.abc_classification_product_level_ids
        )
