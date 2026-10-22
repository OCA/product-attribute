# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Command, Domain

from .common import ABCClassificationLevelCase


class TestProduct(ABCClassificationLevelCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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

        self.assertFalse(self.product_product.abc_classification_product_level_ids)
        self.assertFalse(self.product_template.abc_classification_product_level_ids)

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
            new_variant.abc_classification_product_level_ids,
            product_level,
        )
        self.assertFalse(self.product_template.abc_classification_product_level_ids)

    def test_04(self):
        """
        Data:
            A product template
        Test case:
            Check if resource id in action is the product variant one
        """
        self.product_template.abc_classification_profile_ids = (
            self.classification_profile
        )
        action = self.classification_profile.action_view_products()
        self.assertEqual(action["res_id"], self.product_template.product_variant_ids.id)

    def test_05(self):
        """
        Data:
            A product template with two variants
        Test case:
            Check if doamin in action is the product variants ids
        """
        self._create_variant(self.size_attr_value_m)
        self.product_template.product_variant_ids.abc_classification_profile_ids = (
            self.classification_profile
        )
        action = self.classification_profile.action_view_products()
        # A Domain never compares equal to the list it serialises to, so the
        # expectation is written as one too.
        self.assertEqual(
            action["domain"],
            Domain("id", "in", self.product_template.product_variant_ids.ids),
        )

    def test_06(self):
        """
        Data:
            A product template with one variant
        Test Case:
            Associate a classification profile to the category
        Expected result:
            The variant is associated to the classification profile
        """
        self.product_template.categ_id.abc_classification_profile_ids = (
            self.classification_profile
        )
        self.product_product._onchange_categ_id_abc_classification()
        self.assertEqual(
            self.product_product.abc_classification_profile_ids,
            self.classification_profile,
        )

    def test_07(self):
        """
        Data:
            A product template with one variant
        Test Case:
            1 Create new category
            2 Associate a classification profile to the category
            3 Create new product
        Expected result:
            The product is associated to the classification profile
        """
        new_category = self.env["product.category"].create(
            {"name": "Test Category ABC"}
        )
        new_category.abc_classification_profile_ids = self.classification_profile_bis
        new_template = self.env["product.template"].create(
            {"name": "Test Template ABC", "categ_id": new_category.id}
        )
        self.assertEqual(
            new_template.abc_classification_profile_ids, self.classification_profile_bis
        )

    def test_08(self):
        """
        Data:
            A product template with one variant
        Test Case:
            Move the product to a category holding a classification profile
        Expected result:
            The variant is associated to the classification profile of its new
            category
        """
        new_category = self.env["product.category"].create(
            {"name": "Test Category ABC write"}
        )
        new_category.abc_classification_profile_ids = self.classification_profile
        self.assertFalse(self.product_product.abc_classification_profile_ids)
        self.product_product.write({"categ_id": new_category.id})
        self.assertEqual(
            self.product_product.abc_classification_profile_ids,
            self.classification_profile,
        )

    def test_09(self):
        """
        Data:
            A category holding a classification profile and a product of that
            category already classified with another profile
        Test Case:
            Apply the category profile to its products
        Expected result:
            The profile of the category replaces the one of the product, and
            the products excluded from the category update keep theirs
        """
        category = self.product_template.categ_id
        category.abc_classification_profile_ids = self.classification_profile
        self.product_product.abc_classification_profile_ids = (
            self.classification_profile_bis
        )
        pinned_product = self.env["product.product"].create(
            {
                "name": "Test pinned",
                "categ_id": category.id,
                "abc_classification_profile_updatable_from_category": False,
                "abc_classification_profile_ids": [
                    Command.set(self.classification_profile_bis.ids)
                ],
            }
        )
        category.update_product_abc_classification_profile()
        self.assertEqual(
            self.product_product.abc_classification_profile_ids,
            self.classification_profile,
        )
        self.assertEqual(
            pinned_product.abc_classification_profile_ids,
            self.classification_profile_bis,
        )

    def test_10(self):
        """
        Data:
            A product template with one variant and a level belonging to
            another product
        Test Case:
            Link that level to the template
        Expected result:
            The level is moved to the variant of the template
        """
        other_product = self.env["product.product"].create(
            {"name": "Test other", "company_id": False}
        )
        product_level = self.ProductLevel.create(
            {
                "product_id": other_product.id,
                "manual_level_id": self.classification_level_a.id,
                "profile_id": self.classification_profile.id,
            }
        )
        self.product_template.write(
            {"abc_classification_product_level_ids": [Command.link(product_level.id)]}
        )
        self.assertEqual(product_level.product_id, self.product_product)
        self.assertEqual(
            self.product_product.abc_classification_product_level_ids,
            product_level,
        )

    def test_11(self):
        """
        Data:
            A classification profile
        Test case:
            Count the products of the profile, before and after profiling one
        Expected result:
            The count follows the profiled products
        """
        self.assertEqual(self.classification_profile.product_count, 0)
        self.product_product.abc_classification_profile_ids = (
            self.classification_profile
        )
        self.assertEqual(self.classification_profile.product_count, 1)

    def test_12(self):
        """
        Data:
            A classification profile without any product
        Test case:
            Open the products of the profile
        Expected result:
            The action closes since there is nothing to show
        """
        action = self.classification_profile.action_view_products()
        self.assertEqual(action["type"], "ir.actions.act_window_close")

    def test_13_create_level_from_the_template_form(self):
        """The template form only knows the template, not the variant.

        Its one2many fills `product_tmpl_id`, so the required `product_id` has
        to be deduced from the single variant the page is restricted to.
        """
        self.product_template.write(
            {
                "abc_classification_profile_ids": [
                    Command.set([self.classification_profile.id])
                ],
                "abc_classification_product_level_ids": [
                    Command.create(
                        {
                            "profile_id": self.classification_profile.id,
                            "manual_level_id": self.classification_level_a.id,
                        }
                    )
                ],
            }
        )
        level = self.product_template.abc_classification_product_level_ids
        self.assertEqual(len(level), 1)
        self.assertEqual(level.product_id, self.product_product)
        self.assertEqual(level.product_tmpl_id, self.product_template)

    def test_14_open_variants_from_a_multi_variant_template(self):
        """The template page points at the variants instead of its own fields."""
        self._create_variant(self.size_attr_value_m)
        self.assertGreater(self.product_template.product_variant_count, 1)
        action = self.product_template.action_open_abc_classification_variants()
        self.assertEqual(
            self.env["product.product"].search(action["domain"]),
            self.product_template.product_variant_ids,
        )
