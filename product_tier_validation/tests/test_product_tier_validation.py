# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class TestProductTierValidation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group_ids = cls.env.ref("base.group_system").ids
        cls.test_user_1 = cls.env["res.users"].create(
            {
                "name": "John",
                "login": "test1",
                "groups_id": [(6, 0, group_ids)],
                "email": "test@examlple.com",
            }
        )

        cls.tier_def_obj = cls.env["tier.definition"]
        cls.normal_state = cls.env.ref("product_state.product_state_sellable")

    def test_tier_validation_model_name(self):
        self.assertIn(
            "product.template", self.tier_def_obj._get_tier_validation_model_names()
        )

    def test_validation_product_template(self):
        product = self.env["product.template"].create(
            {
                "name": "Product for test",
                "list_price": 120.00,
            }
        )
        product.request_validation()
        product.with_user(self.test_user_1).validate_tier()
        product.write({"product_state_id": self.normal_state.id})
        self.assertEqual(product.state, self.normal_state.code)
