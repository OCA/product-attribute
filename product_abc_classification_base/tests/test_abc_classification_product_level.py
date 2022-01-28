# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from .common import ABCClassificationLevelCase
from odoo.exceptions import ValidationError


class TestABCClassificationProductLevel(ABCClassificationLevelCase):
    @classmethod
    def setUpClass(cls):
        super(TestABCClassificationProductLevel, cls).setUpClass()
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test 1",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )
        cls.product_level = cls.ProductLevel.create(
            {
                "product_id": cls.product_product.id,
                "computed_level_id": cls.classification_level_a.id,
                "profile_id": cls.classification_profile.id
            }
        )

    @classmethod
    def _create_product_levels(cls):
        product_2 = cls.env["product.product"].create(
            {
                "name": "Test 2",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )

        product_3 = cls.env["product.product"].create(
            {
                "name": "Test 3",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )
        cls.ProductLevel.create(
            {
                "product_id": product_2.id,
                "manual_level_id": cls.classification_level_b.id,
                "computed_level_id": cls.classification_level_a.id,
                "profile_id": cls.classification_profile.id
            }
        )
        cls.ProductLevel.create(
            {
                "product_id": product_3.id,
                "manual_level_id": cls.classification_level_b.id,
                "computed_level_id": cls.classification_level_a.id,
                "profile_id": cls.classification_profile.id
            }
        )

    def test_00(self):
        """
        Test case:
            Create a classification product level with only a computed_level_id
        Expected result:
            A instance is created with:
             * the manual_level_id and level_id set
             * flag is False since manual and computd are the same

        """
        level = self.ProductLevel.create(
            {
                "product_id": self.product_1.id,
                "computed_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id
            }
        )
        self.assertEqual(level.manual_level_id, self.classification_level_a)
        self.assertEqual(level.level_id, self.classification_level_a)
        self.assertFalse(level.flag)

    def test_01(self):
        """
        Test case:
            Create product level with only a manual level

            A creation if a product level is created without computed value
            the computed value is never taken into account
        Expected result:
            A new level is create with:
            * computed_level_id = False
            * level_id = manual_level_id
            * flag = False
        """
        level = self.ProductLevel.create(
            {
                "product_id": self.product_1.id,
                "manual_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id
            }
        )
        self.assertFalse(level.computed_level_id)
        self.assertEqual(level.manual_level_id, self.classification_level_a)
        self.assertEqual(level.level_id, self.classification_level_a)
        self.assertFalse(level.flag)

    def test_02(self):
        """
        Data:
            An existing classification level with computed = manual
        Test case:
            1. Change manual_level_id to an other value than the computed one
            2. Reset manual_level_id to the computed one
        Expected result:
            1. level_id === manual =! computed and flag is true
            2  level_id == manual == computed and flag is true
            ValidationError
        """
        self.assertFalse(self.product_level.flag)
        self.assertEqual(
            self.product_level.manual_level_id,
            self.product_level.computed_level_id,
        )
        self.assertEqual(
            self.product_level.computed_level_id, self.classification_level_a
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_a
        )
        # 1
        self.product_level.manual_level_id = self.classification_level_b
        self.assertEqual(
            self.product_level.level_id, self.classification_level_b
        )
        self.assertTrue(self.product_level.flag)
        # 2
        self.product_level.manual_level_id = (
            self.product_level.computed_level_id
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_a
        )
        self.assertFalse(self.product_level.flag)

    def test_03(self):
        """
        Data:
            An existing product level
        Test case:
            Create a new product level for the same product and the same profile
        Expected result:
            IntegrityError (level name must be unique by profile and product)
        """
        with self.assertRaises(IntegrityError):
            self.ProductLevel.create(
                {
                    "product_id": self.product_product.id,
                    "computed_level_id": self.classification_level_a.id,
                    "profile_id": self.classification_profile.id
                }
            )

    def test_04(self):
        """
        Data:
            An existing product level
        Test case:
            1. Link a manual level from an other profile
            2. Link a computed level from an other profile
        Expected result:
            1. and 2. Validation error (All the levels must share the same
            profile as the one on the product level)
        """
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.product_level.write({
                "manual_level_id": self.classification_level_b.id,
                "computed_level_id": self.classification_level_bis_a.id
            })
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.product_level.write({
                "manual_level_id": self.classification_level_bis_a.id,
                "computed_level_id": self.classification_level_a.id
            })
        self.product_level.write({
            "manual_level_id": self.classification_level_bis_a.id,
            "computed_level_id": self.classification_level_bis_a.id,
            "profile_id": self.classification_profile_bis.id
        })

    def test_05(self):
        """
        Test case:
            Create a product level without computed nor manual level
        Expected result:
            Validation error (at least a value for one of these fields is
            expected)
        """
        with self.assertRaises(ValidationError):
            self.ProductLevel.create(
                {
                    "product_id": self.product_1.id,
                    "profile_id": self.classification_profile.id
                }
            )

    def test_06_update_product_level_with_auto_compute(self):
        self.classification_profile_bis.auto_apply_computed_value = True
        self.product_level.write({
            "computed_level_id": self.classification_level_bis_a.id,
            "profile_id": self.classification_profile_bis.id
        })

        self.assertEqual(
            self.product_level.manual_level_id,
            self.product_level.computed_level_id,
        )
        self.assertEqual(
            self.product_level.computed_level_id, self.classification_level_bis_a
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_bis_a
        )

        self.product_level.write({
            "computed_level_id": self.classification_level_bis_b.id,
        })
        self.assertEqual(
            self.product_level.manual_level_id,
            self.product_level.computed_level_id,
        )
        self.assertEqual(
            self.product_level.computed_level_id, self.classification_level_bis_b
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_bis_b
        )

    def test_07_update_product_level_without_auto_compute(self):
        self.classification_profile.auto_apply_computed_value = False
        self.product_level.write({
            "manual_level_id": self.classification_level_b.id,
            "computed_level_id": self.classification_level_a.id,
            "profile_id": self.classification_profile.id
        })

        self.assertNotEqual(
            self.product_level.manual_level_id,
            self.product_level.computed_level_id,
        )
        self.assertEqual(
            self.product_level.computed_level_id, self.classification_level_a
        )
        self.assertEqual(
            self.product_level.manual_level_id, self.classification_level_b
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_b
        )


        self.product_level.write({
            "manual_level_id": self.classification_level_a.id,
            "computed_level_id": self.classification_level_b.id,
        })


        self.assertNotEqual(
            self.product_level.manual_level_id,
            self.product_level.computed_level_id,
        )
        self.assertEqual(
            self.product_level.computed_level_id, self.classification_level_b
        )
        self.assertEqual(
            self.product_level.manual_level_id, self.classification_level_a
        )
        self.assertEqual(
            self.product_level.level_id, self.classification_level_a
        )

    def test_08_update_recordset_with__autocompute(self):
        self._create_product_levels()
        self.classification_profile.auto_apply_computed_value = True

        levels = self.ProductLevel.search([("profile_id", "=", self.classification_profile.id)])
        levels.write({
            "manual_level_id": self.classification_level_a.id,
            "computed_level_id": self.classification_level_b.id,
        })

        for level in levels:
            self.assertEqual(level.manual_level_id, level.computed_level_id)
            self.assertEqual(level.manual_level_id, self.classification_level_b)
            self.assertEqual(level.computed_level_id, self.classification_level_b)
            self.assertEqual(level.level_id, self.classification_level_b)

    def test_09_update_recordset_and_change_profile(self):
        self._create_product_levels()
        self.classification_profile_bis.auto_apply_computed_value = True

        levels = self.ProductLevel.search([("profile_id", "=", self.classification_profile.id)])
        levels.write({
            "computed_level_id": self.classification_level_bis_a.id,
            "profile_id": self.classification_profile_bis.id

        })

        for level in levels:
            self.assertEqual(level.manual_level_id, level.computed_level_id)
            self.assertEqual(level.manual_level_id, self.classification_level_bis_a)
            self.assertEqual(level.computed_level_id, self.classification_level_bis_a)
            self.assertEqual(level.level_id, self.classification_level_bis_a)

    def test_10_create_product_level_for_profile_auto_assign(self):
        self.classification_profile.auto_apply_computed_value = True
        level = self.ProductLevel.create(
            {
                "product_id": self.product_1.id,
                "manual_level_id": self.classification_level_b.id,
                "computed_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id
            }
        )
        self.assertEqual(level.manual_level_id, level.computed_level_id)
        self.assertEqual(level.manual_level_id, self.classification_level_a)
        self.assertEqual(level.computed_level_id, self.classification_level_a)
        self.assertEqual(level.level_id, self.classification_level_a)

    def test_11_auto_apply_computed_level(self):
        self._create_product_levels()

        levels = self.ProductLevel.search([("profile_id", "=", self.classification_profile.id)])
        level0 = levels[0]
        level1 = levels[1]
        level2 = levels[2]
        self.assertEqual(level0.manual_level_id, level0.computed_level_id)
        self.assertEqual(level0.manual_level_id, self.classification_level_a)
        self.assertEqual(level0.computed_level_id, self.classification_level_a)
        self.assertEqual(level0.level_id, self.classification_level_a)

        self.assertNotEqual(level1.manual_level_id, level1.computed_level_id)
        self.assertEqual(level1.manual_level_id, self.classification_level_b)
        self.assertEqual(level1.computed_level_id, self.classification_level_a)
        self.assertEqual(level1.level_id, self.classification_level_b)

        self.assertNotEqual(level2.manual_level_id, level2.computed_level_id)
        self.assertEqual(level2.manual_level_id, self.classification_level_b)
        self.assertEqual(level2.computed_level_id, self.classification_level_a)
        self.assertEqual(level2.level_id, self.classification_level_b)

        self.classification_profile.auto_apply_computed_value = True
        for level in levels:
            self.assertEqual(level.manual_level_id, self.classification_level_a)
            self.assertEqual(level.computed_level_id, self.classification_level_a)
            self.assertEqual(level.level_id, self.classification_level_a)
