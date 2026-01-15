# Copyright 2025 360ERP (https://www.360erp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from unittest.mock import patch

from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase


class TestProductProfile(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product1 = cls.env["product.product"].create({"name": "_1"})
        cls.product2 = cls.env["product.product"].create({"name": "_1"})

        cls.profile_consu = cls.env["product.profile"].create(
            {
                "name": "Profile Consu",
                "sequence": 0,
                "explanation": "_1",
                "type": "consu",
            }
        )
        cls.profile_service = cls.env["product.profile"].create(
            {
                "name": "Profile Service",
                "sequence": 0,
                "explanation": "_1",
                "type": "service",
            }
        )
        cls.group = cls.env.ref("product_profile.group_product_profile_user")

    def test_create_product(self):
        self.assertEqual(
            self.env["product.template"]
            .create(
                {
                    "name": __name__,
                    "profile_id": self.profile_consu.id,
                },
            )
            .type,
            "consu",
        )
        self.assertEqual(
            self.env["product.template"]
            .create(
                {
                    "name": __name__,
                    "profile_id": self.profile_service.id,
                },
            )
            .type,
            "service",
        )

    def test_create_product_variant(self):
        self.assertEqual(
            self.env["product.product"]
            .create(
                {
                    "name": __name__,
                    "profile_id": self.profile_consu.id,
                },
            )
            .type,
            "consu",
        )
        self.assertEqual(
            self.env["product.product"]
            .create(
                {
                    "name": __name__,
                    "profile_id": self.profile_service.id,
                },
            )
            .type,
            "service",
        )

    def test_write_product(self):
        product = self.env["product.template"].create(
            {
                "name": __name__,
                "profile_id": self.profile_consu.id,
            },
        )
        self.assertEqual(product.type, "consu")
        product.write(
            {
                "profile_id": self.profile_service.id,
                "name": "TESTX",
            },
        )
        self.assertEqual(product.type, "service")
        self.assertEqual(product.name, "TESTX")

    def test_write_product_variant(self):
        product = self.env["product.product"].create(
            {
                "name": __name__,
                "profile_id": self.profile_consu.id,
            },
        )
        self.assertEqual(product.type, "consu")
        product.write(
            {
                "profile_id": self.profile_service.id,
                "name": "TESTX",
            },
        )
        self.assertEqual(product.type, "service")
        self.assertEqual(product.name, "TESTX")

    def test_onchange_product_variant(self):
        product = self.env["product.product"].create(
            {
                "name": __name__,
                "profile_id": self.profile_consu.id,
            },
        )
        product_form = Form(product)
        product_form.profile_id = self.profile_service
        self.assertEqual(product_form.type, "service")
        # Values are not unset after resetting profile
        product_form.profile_id = self.env["product.profile"]
        self.assertEqual(product_form.type, "service")

    def test_onchange_exception_handling(self):
        product = self.env["product.product"].create(
            {
                "name": __name__,
                "profile_id": self.profile_consu.id,
            },
        )
        product_form = Form(product)
        with patch.object(
            type(product),
            "_get_vals_from_profile",
            autospec=True,
            return_value={"type": "invalid"},
        ):
            with self.assertRaisesRegex(
                UserError, "Wrong value for product.template.type: 'invalid'"
            ):
                product_form.profile_id = self.profile_service

    def test_product_variant_write_profile(self):
        product = self.env["product.product"].create(
            {
                "name": __name__,
                "profile_id": self.profile_service.id,
            }
        )
        self.assertEqual(product.type, "service")
        self.profile_service.write(
            {
                "type": "consu",
                "name": "New Name",
            }
        )
        self.assertEqual(product.type, "consu")
        # Name field is not propagated to product
        self.assertEqual(product.name, __name__)

    def test_product_write_profile(self):
        product = self.env["product.template"].create(
            {
                "name": __name__,
                "profile_id": self.profile_service.id,
            }
        )
        self.assertEqual(product.type, "service")
        self.profile_service.type = "consu"
        self.assertEqual(product.type, "consu")

    def test_product_variant_with_group(self):
        """Users in the profile group can see, but not set profile fields"""
        self.env.user.groups_id += self.group
        res = self.env["product.product"].get_view(view_type="form")
        root = etree.fromstring(res["arch"])
        field = root.find(".//field[@name='type']")
        self.assertTrue(field is not None)
        self.assertEqual(field.attrib["readonly"], "profile_id")

    def test_product_variant_without_group(self):
        """Users not in the profile group cannot see the fields if profile is set"""
        self.env.user.groups_id -= self.group
        self.assertNotIn(self.group, self.env.user.groups_id)
        res = self.env["product.product"].get_view(view_type="form")
        root = etree.fromstring(res["arch"])
        field = root.find(".//field[@name='type']")
        self.assertTrue(field is not None)
        self.assertEqual(field.attrib["invisible"], "profile_id")

    def test_product_variant_easy_view(self):
        self.env["product.product"].get_view(
            view_id=self.env.ref("product.product_variant_easy_edit_view").id,
            view_type="form",
        )

    def test_product_get_view(self):
        self.env["product.template"].get_view(view_type="form")

    def test_product_tmpl_get_view(self):
        """Profiles are injected as search filters"""
        view_id = self.env.ref("product.product_template_search_view").id
        res = self.env["product.template"].get_view(view_id=view_id, view_type="search")
        self.assertIn(b'string="Profile Consu"', res["arch"])

    def test_profiles_to_filter(self):
        self.assertIn(
            self.profile_service.id,
            dict(self.env["product.product"]._get_profiles_to_filter()),
        )
        self.assertIn(
            self.profile_consu.id,
            dict(self.env["product.product"]._get_profiles_to_filter()),
        )
        self.assertIn(
            self.profile_service.id,
            dict(
                self.env["product.product"]._get_profiles_to_filter(
                    [("id", "!=", self.profile_consu.id)]
                )
            ),
        )
        self.assertNotIn(
            self.profile_consu.id,
            dict(
                self.env["product.product"]._get_profiles_to_filter(
                    [("id", "!=", self.profile_consu.id)]
                )
            ),
        )

    def test_product_profile_get_view(self):
        self.env["product.profile"].get_view(view_type="form")
