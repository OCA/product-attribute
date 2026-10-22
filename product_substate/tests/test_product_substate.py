# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductSubstate(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_state_draft = cls.env.ref("product_state.product_state_draft")
        cls.product_state_sellable = cls.env.ref("product_state.product_state_sellable")
        # ``product_status`` computes the state from dates and deactivates the
        # ``draft`` state: use its ``new`` state as the other state then.
        cls.has_product_status = "new_until" in cls.env["product.template"]._fields
        cls.other_state = "new" if cls.has_product_status else "draft"
        substate_type = cls.env.ref("product_substate.base_substate_type_product")
        TargetStateValue = cls.env["target.state.value"]
        target_other = TargetStateValue.search(
            [
                ("base_substate_type_id", "=", substate_type.id),
                ("target_state_value", "=", cls.other_state),
            ],
            limit=1,
        ) or TargetStateValue.create(
            {
                "name": cls.other_state,
                "base_substate_type_id": substate_type.id,
                "target_state_value": cls.other_state,
            }
        )
        target_sellable = cls.env.ref("product_substate.target_state_value_sellable")
        Substate = cls.env["base.substate"]
        cls.substate_other = Substate.create(
            {
                "name": "Test Other",
                "sequence": -10,
                "target_state_value_id": target_other.id,
            }
        )
        cls.substate_sellable_instock = Substate.create(
            {
                "name": "Test In Stock",
                "sequence": -10,
                "target_state_value_id": target_sellable.id,
            }
        )
        cls.substate_sellable_onorder = Substate.create(
            {
                "name": "Test On Order",
                "sequence": -5,
                "target_state_value_id": target_sellable.id,
            }
        )
        cls.product = cls.env["product.template"].create({"name": "Test Product"})

    def _set_other_state(self, product):
        if self.has_product_status:
            product.new_until = fields.Date.today() + timedelta(days=10)
        else:
            product.product_state_id = self.product_state_draft

    def _set_sellable_state(self, product):
        if self.has_product_status:
            product.new_until = False
        else:
            product.product_state_id = self.product_state_sellable

    def test_default_substate(self):
        self.assertEqual(self.product.state, "sellable")
        self.assertEqual(self.product.substate_id, self.substate_sellable_instock)

    def test_create_with_state(self):
        if self.has_product_status:
            self.skipTest("product_status computes the state from dates")
        product = self.env["product.template"].create(
            {"name": "Draft Product", "product_state_id": self.product_state_draft.id}
        )
        self.assertEqual(product.state, "draft")
        self.assertEqual(product.substate_id, self.substate_other)

    def test_product_substate_flow(self):
        """Check the whole substate flow."""
        # Block substate not corresponding to the current state
        with self.assertRaises(ValidationError):
            self.product.substate_id = self.substate_other

        # Switch between substates of the same state
        self.product.substate_id = self.substate_sellable_onorder
        self.assertEqual(self.product.substate_id, self.substate_sellable_onorder)

        # Changing the state sets the default substate of the new state
        self._set_other_state(self.product)
        self.assertEqual(self.product.state, self.other_state)
        self.assertEqual(self.product.substate_id, self.substate_other)

        with self.assertRaises(ValidationError):
            self.product.substate_id = self.substate_sellable_instock

        self._set_sellable_state(self.product)
        self.assertEqual(self.product.state, "sellable")
        self.assertEqual(self.product.substate_id, self.substate_sellable_instock)
