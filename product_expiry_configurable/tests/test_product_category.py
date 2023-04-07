# Copyright 2022 Creu Blanca
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase

from .common import ProductExpiryCategoryCommon


class TestProductCategory(ProductExpiryCategoryCommon, TransactionCase):
    def check_fields(self, categs, expected_values, children=True):
        """

        Check that a value modification on a root category is
        transmitted to all children.
        """
        for categ in categs:
            for field, value in expected_values:
                self.assertEqual(
                    value,
                    getattr(categ, field),
                    msg=f"The field {field} on category {categ.name} is not correct!",
                )
            if children:
                self.check_fields(categ.child_id, expected_values=expected_values)

    def test_modify_root_category(self):
        """
        Test Case:
            Set dates on root category
            Create a category that has that root as parent
            Check the corresponding dates are same

            Then, modify some dates on the child category and check
            they remain.
        """
        self.categ_lvl_1.update(
            {
                "alert_time": 3,
                "removal_time": 2,
                "use_time": 1,
                "expiration_time": 5,
            }
        )

        expected_values = [
            ("alert_time", 3),
            ("removal_time", 2),
            ("use_time", 1),
            ("expiration_time", 5),
        ]

        self.check_fields(self.categ_lvl_1, expected_values)

        expected_values = [
            ("alert_time", 4),
            ("removal_time", 3),
            ("use_time", 2),
            ("expiration_time", 6),
        ]

        self.categ_lvl_1_1.write(
            {
                "alert_time": 4,
                "removal_time": 3,
                "use_time": 2,
                "expiration_time": 6,
            }
        )

        self.check_fields(self.categ_lvl_1_1, expected_values, False)

    def test_modify_root_category_use(self):
        """
        Modify the parent category use_expiration_date field
        Children should not be modified.
        Create a new category with the parent here above.
        The field use_expiration_date should be True

        """

        self.categ_lvl_1_1.write(
            {
                "use_expiration_date": True,
            }
        )
        self.assertFalse(self.categ_lvl_1_1_1.use_expiration_date)

        self.categ_lvl_1_1_2 = self.ProductCategory.create(
            {
                "name": "Category 2",
                "parent_id": self.categ_lvl_1_1.id,
            }
        )

        self.assertTrue(self.categ_lvl_1_1_2.use_expiration_date)
