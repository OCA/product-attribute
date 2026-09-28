# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestProductCategoryLevel(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.print_category_parent = cls.env.ref(
            "product_category_level.demo_category_parent"
        )
        cls.print_category_child_1 = cls.env.ref(
            "product_category_level.demo_category_child_1"
        )
        cls.print_category_child_2 = cls.env.ref(
            "product_category_level.demo_category_child_2"
        )

    def test_product_category_level(self):
        self.assertEqual(2, self.print_category_child_2.level)
        self.assertEqual(0, self.print_category_parent.level)
        self.assertEqual(1, self.print_category_child_1.level)
