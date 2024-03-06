# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests.common import Form, TransactionCase, new_test_user


class TestProductCostSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_edit_cost_group_id = cls.env.ref(
            "product_cost_security.group_product_edit_cost"
        ).id
        cls.product_cost_group_id = cls.env.ref(
            "product_cost_security.group_product_cost"
        ).id
        cls.product_template_model = cls.env["product.template"].with_context(
            tracking_disable=True
        )
        cls.env.user.write(
            {
                "groups_id": [
                    (6, 0, cls.env.ref("base.group_system").ids),
                ],
            }
        )

    def test_without_access_to_product_costs_group(self):
        sheet_form = Form(self.product_template_model.with_user(self.env.user))
        sheet_form.name = "Test Product"
        sheet_form.save()
        with self.assertRaises(AssertionError):
            # It would raise an AssertionError as the field would not be found in the view
            # as the user does not have the group- Access to product costs
            standard_price = sheet_form.standard_price
            self.assertEqual(standard_price, 0.0)

    def test_with_access_to_product_costs_group(self):
        self.env.user.groups_id = [
            (
                6,
                0,
                [self.product_cost_group_id],
            )
        ]
        sheet_form = Form(self.product_template_model.with_user(self.env.user))
        sheet_form.name = "Test Product"
        sheet_form.save()
        standard_price = (
            sheet_form.standard_price
        )  # It would not raise any error now as the user
        # has the required group to view the costs
        self.assertEqual(standard_price, 0.0)

    def test_without_access_to_modify_product_costs_group(self):
        sheet_form = Form(self.product_template_model.with_user(self.env.user))
        sheet_form.name = "Test Product"
        sheet_form.save()
        with self.assertRaises(AssertionError):
            # It would raise an AssertionError as the field is readonlyin the view
            # as the user does not have the group- Modify product costs
            sheet_form.standard_price = 5.0

    def test_with_access_to_modify_product_costs_group(self):
        self.env.user.groups_id = [
            (
                6,
                0,
                [self.product_edit_cost_group_id],
            )
        ]
        sheet_form = Form(self.product_template_model.with_user(self.env.user))
        sheet_form.name = "Test Product"
        sheet_form.save()
        sheet_form.standard_price = 5.0  # It would not raise any error now as the user
        # has the required group to modify the costs
        self.assertEqual(sheet_form.standard_price, 5.0)

    def test_api_modification(self):
        """Test that a direct API call respects the security groups."""
        # Using base.group_system because it's the only group in this module's
        # dependency graph with CRUD access to products
        editor = new_test_user(
            self.env,
            "editor",
            groups="base.group_system,product_cost_security.group_product_edit_cost",
        )
        reader = new_test_user(
            self.env,
            "reader",
            groups="base.group_system,product_cost_security.group_product_cost",
        )
        user = new_test_user(self.env, "user", groups="base.group_system")
        # Editor can write and read
        product = (
            self.env["product.product"]
            .with_user(editor)
            .create(
                {
                    "name": "Test product",
                    "standard_price": 10.0,
                }
            )
        )
        self.assertEqual(
            product.read(["standard_price"]),
            [{"id": product.id, "standard_price": 10.0}],
        )
        product.standard_price = 20.0
        self.assertEqual(
            product.read(["standard_price"]),
            [{"id": product.id, "standard_price": 20.0}],
        )
        # Reader can read but not write
        product = product.with_user(reader)
        with self.assertRaises(AccessError):
            product.standard_price = 30.0
        self.assertEqual(
            product.read(["standard_price"]),
            [{"id": product.id, "standard_price": 20.0}],
        )
        # User can't read or write (standard Odoo when setting field groups)
        product = product.with_user(user)
        with self.assertRaises(AccessError):
            product.standard_price = 30.0
        with self.assertRaises(AccessError):
            product.read(["standard_price"])
        # Sudo still works
        product.sudo().standard_price = 30.0
        self.assertEqual(
            product.sudo().read(["standard_price"]),
            [{"id": product.id, "standard_price": 30.0}],
        )
