# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import new_test_user
from odoo.tests.common import TransactionCase


class TestProductVisibilityByUserGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_a = cls.env["res.groups"].create({"name": "Product A"})
        cls.group_b = cls.env["res.groups"].create({"name": "Product B"})
        cls.user_a = new_test_user(cls.env, "user_a", "base.group_user")
        cls.user_b = new_test_user(cls.env, "user_b", "base.group_user")
        cls.user_without_visibility_group = new_test_user(
            cls.env, "user_without_visibility_group", "base.group_user"
        )
        cls.portal_user = new_test_user(cls.env, "portal_user", "base.group_portal")
        cls.product_manager = new_test_user(
            cls.env,
            "product_manager",
            "base.group_user,product.group_product_manager",
        )
        # grant portal read access, so the test validates record rules
        cls.env["ir.model.access"].create(
            [
                {
                    "name": "product.template portal read test",
                    "model_id": cls.env.ref("product.model_product_template").id,
                    "group_id": cls.env.ref("base.group_portal").id,
                    "perm_read": True,
                    "perm_write": False,
                    "perm_create": False,
                    "perm_unlink": False,
                },
                {
                    "name": "product.product portal read test",
                    "model_id": cls.env.ref("product.model_product_product").id,
                    "group_id": cls.env.ref("base.group_portal").id,
                    "perm_read": True,
                    "perm_write": False,
                    "perm_create": False,
                    "perm_unlink": False,
                },
            ]
        )
        cls.user_a.group_ids = [Command.link(cls.group_a.id)]
        cls.user_b.group_ids = [Command.link(cls.group_b.id)]
        cls.public_template = (
            cls.env["product.template"].sudo().create({"name": "Public Product"})
        )
        cls.internal_template = cls.env["product.template"].create(
            {
                "name": "Internal Product",
                "visibility_group_ids": [
                    Command.link(cls.env.ref("base.group_user").id)
                ],
            }
        )
        cls.group_a_template = cls.env["product.template"].create(
            {
                "name": "Group A Product",
                "visibility_group_ids": [Command.link(cls.group_a.id)],
            }
        )
        cls.group_b_template = cls.env["product.template"].create(
            {
                "name": "Group B Product",
                "visibility_group_ids": [Command.link(cls.group_b.id)],
            }
        )

    def test_product_template_visibility_by_user_group(self):
        """products without groups are visible, products with groups are restricted"""
        product_templates = (
            self.public_template
            | self.internal_template
            | self.group_a_template
            | self.group_b_template
        )

        self.assertEqual(
            self.env["product.template"]
            .with_user(self.user_a)
            .search([("id", "in", product_templates.ids)]),
            self.public_template | self.internal_template | self.group_a_template,
        )
        self.assertEqual(
            self.env["product.template"]
            .with_user(self.user_b)
            .search([("id", "in", product_templates.ids)]),
            self.public_template | self.internal_template | self.group_b_template,
        )
        self.assertEqual(
            self.env["product.template"]
            .with_user(self.user_without_visibility_group)
            .search([("id", "in", product_templates.ids)]),
            self.public_template | self.internal_template,
        )
        self.assertEqual(
            self.env["product.template"]
            .with_user(self.product_manager)
            .search([("id", "in", product_templates.ids)]),
            product_templates,
        )

    def test_product_variant_visibility_by_user_group(self):
        """variant visibility follows the template visibility groups"""
        products = (
            self.public_template.product_variant_id
            | self.internal_template.product_variant_id
            | self.group_a_template.product_variant_id
            | self.group_b_template.product_variant_id
        )

        self.assertEqual(
            self.env["product.product"]
            .with_user(self.user_a)
            .search([("id", "in", products.ids)]),
            self.public_template.product_variant_id
            | self.internal_template.product_variant_id
            | self.group_a_template.product_variant_id,
        )
        self.assertEqual(
            self.env["product.product"]
            .with_user(self.user_b)
            .search([("id", "in", products.ids)]),
            self.public_template.product_variant_id
            | self.internal_template.product_variant_id
            | self.group_b_template.product_variant_id,
        )
        self.assertEqual(
            self.env["product.product"]
            .with_user(self.user_without_visibility_group)
            .search([("id", "in", products.ids)]),
            self.public_template.product_variant_id
            | self.internal_template.product_variant_id,
        )
        self.assertEqual(
            self.env["product.product"]
            .with_user(self.product_manager)
            .search([("id", "in", products.ids)]),
            products,
        )

    def test_portal_user_cannot_see_internal_product(self):
        """portal users cannot see products limited to internal users"""
        product_templates = self.public_template | self.internal_template
        products = (
            self.public_template.product_variant_id
            | self.internal_template.product_variant_id
        )

        self.assertEqual(
            self.env["product.template"]
            .with_user(self.portal_user)
            .search([("id", "in", product_templates.ids)]),
            self.public_template,
        )
        self.assertEqual(
            self.env["product.product"]
            .with_user(self.portal_user)
            .search([("id", "in", products.ids)]),
            self.public_template.product_variant_id,
        )

    def test_implied_user_groups_are_used_for_visibility(self):
        """users can see products linked to implied groups"""
        implied_group = self.env["res.groups"].create(
            {
                "name": "Product Visibility Implied",
                "implied_ids": [Command.link(self.group_a.id)],
            }
        )
        implied_user = new_test_user(
            self.env, "product_visibility_implied", "base.group_user"
        )
        implied_user.group_ids = [Command.link(implied_group.id)]

        self.assertEqual(
            self.env["product.template"]
            .with_user(implied_user)
            .search([("id", "in", self.group_a_template.ids)]),
            self.group_a_template,
        )
