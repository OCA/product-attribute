# Copyright 2026 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import tagged

from .common import ABCClassificationLevelCase


@tagged("post_install", "-at_install")
class TestMultiCompany(ABCClassificationLevelCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create({"name": "Company A"})
        cls.company_b = cls.env["res.company"].create({"name": "Company B"})
        cls.product_in_a = cls.env["product.product"].create(
            {"name": "Prod A", "company_id": cls.company_a.id}
        )
        cls.product_in_b = cls.env["product.product"].create(
            {"name": "Prod B", "company_id": cls.company_b.id}
        )
        cls.product_shared = cls.env["product.product"].create({"name": "Prod Shared"})

    def test_shared_profile_inherits_product_company(self):
        self.classification_profile.company_id = False
        self.product_in_a.abc_classification_profile_ids = self.classification_profile
        self.classification_profile._compute_abc_classification()
        level = self.ProductLevel.search(
            [
                ("profile_id", "=", self.classification_profile.id),
                ("product_id", "=", self.product_in_a.id),
            ]
        )
        self.assertEqual(level.company_id, self.company_a)

    def test_company_profile_overrides_product_company(self):
        self.classification_profile.company_id = self.company_a
        self.product_shared.abc_classification_profile_ids = self.classification_profile
        self.classification_profile._compute_abc_classification()
        level = self.ProductLevel.search(
            [
                ("profile_id", "=", self.classification_profile.id),
                ("product_id", "=", self.product_shared.id),
            ]
        )
        self.assertEqual(level.company_id, self.company_a)

    def test_profile_constraint_conflicting_products(self):
        self.product_in_b.abc_classification_profile_ids = self.classification_profile
        with self.assertRaises(ValidationError):
            self.classification_profile.company_id = self.company_a

    def test_level_blocks_conflicting_profile_and_product(self):
        self.classification_profile.company_id = self.company_a
        with self.assertRaises(UserError):
            self.ProductLevel.create(
                {
                    "profile_id": self.classification_profile.id,
                    "product_id": self.product_in_b.id,
                    "manual_level_id": self.classification_level_a.id,
                }
            )

    def test_cannot_change_product_company_with_conflicting_profile(self):
        self.classification_profile.company_id = self.company_a
        self.product_shared.abc_classification_profile_ids = self.classification_profile
        with self.assertRaises(UserError):
            self.product_shared.company_id = self.company_b

    def test_level_company_recomputes_on_profile_change(self):
        self.classification_profile.company_id = False
        self.product_shared.abc_classification_profile_ids = self.classification_profile
        self.classification_profile._compute_abc_classification()
        level = self.ProductLevel.search(
            [
                ("profile_id", "=", self.classification_profile.id),
                ("product_id", "=", self.product_shared.id),
            ]
        )
        self.assertFalse(level.company_id)
        self.classification_profile.company_id = self.company_a
        self.assertEqual(level.company_id, self.company_a)
