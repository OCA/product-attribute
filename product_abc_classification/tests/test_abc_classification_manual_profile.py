# Copyright 2025 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import ABCClassificationLevelCase


class TestABCClassificationProductLevel(ABCClassificationLevelCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_template.abc_classification_profile_ids = cls.classification_profile

    def test_abc_classification_manual_profile(self):
        """
        Test case:
            Execute ABC classification compute for manual (default) profile
        Expected result:
            A instance is created with:
             * the manual_level_id and level_id set
             * computed_level_id is not set

        """
        self.classification_profile._compute_abc_classification()
        level = self.product_product.abc_classification_product_level_ids
        self.assertTrue(level)
        self.assertEqual(level.manual_level_id, self.classification_level_a)
        self.assertEqual(level.level_id, self.classification_level_a)
        self.assertFalse(level.computed_level_id)
