# Copyright 2026 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.fields import Domain
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
        cls.product_shared = cls.env["product.product"].create(
            {"name": "Prod Shared", "company_id": False}
        )

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

    def test_shared_product_takes_a_company_profile(self):
        """A product shared between companies can be classified by one of them.

        Products carry no company by default in Odoo, so refusing this would
        leave a company owned profile with nothing to classify.
        """
        self.classification_profile.company_id = self.company_a
        self.product_shared.abc_classification_profile_ids = self.classification_profile
        self.product_shared.flush_recordset()
        self.assertEqual(
            self.product_shared.abc_classification_profile_ids,
            self.classification_profile,
        )

    def test_template_and_variant_agree_on_a_company_profile(self):
        """The same enrolment, written on the template rather than the variant.

        Only product.template has _check_company_auto, so the two used to give
        opposite answers to the very same operation.
        """
        self.classification_profile.company_id = self.company_a
        template = self.product_shared.product_tmpl_id
        template.abc_classification_profile_ids = self.classification_profile
        template.flush_recordset()
        self.assertEqual(
            self.product_shared.abc_classification_profile_ids,
            self.classification_profile,
        )

    def test_shared_product_takes_one_profile_per_company(self):
        """The reason it is allowed: one product classified once per company.

        Each level belongs to the company of its profile, which is what lets
        the same product be an A mover for one company and a C mover for the
        other. The two coexist because the unique key is per profile.
        """
        self.classification_profile.company_id = self.company_a
        self.classification_profile_bis.company_id = self.company_b
        profiles = self.classification_profile | self.classification_profile_bis
        self.product_shared.abc_classification_profile_ids = profiles
        profiles._compute_abc_classification()
        levels = self.ProductLevel.sudo().search(
            Domain("product_id", "=", self.product_shared.id)
        )
        self.assertEqual(len(levels), 2)
        self.assertEqual(
            set(levels.mapped("company_id").ids),
            {self.company_a.id, self.company_b.id},
        )

    def test_enrolling_a_product_of_another_company_is_refused(self):
        """A/B is still refused, and now from the product side too.

        product.product has no _check_company_auto, so this write used to go
        through unchecked whatever check_company said.
        """
        self.classification_profile.company_id = self.company_a
        with self.assertRaises(ValidationError):
            self.product_in_b.abc_classification_profile_ids = (
                self.classification_profile
            )

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
