# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestProductStateHistory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductTemplate = cls.env["product.template"]
        cls.Wizard = cls.env["product.state.change.wizard"]
        cls.state_sellable = cls.env.ref("product_state.product_state_sellable")
        cls.state_end = cls.env.ref("product_state.product_state_end")
        cls.product = cls.ProductTemplate.create({"name": "Product State History Test"})

    def _change_state(self, product, new_state, reason="Test reason"):
        return self.Wizard.create(
            {
                "product_tmpl_id": product.id,
                "new_state_id": new_state.id,
                "reason": reason,
            }
        ).action_apply()

    def _create_internal_user(self, login, groups=()):
        group_ids = [self.env.ref("base.group_user").id]
        group_ids.extend(group.id for group in groups)
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "group_ids": [Command.set(group_ids)],
            }
        )

    def test_wizard_changes_state_and_creates_history(self):
        self._change_state(self.product, self.state_end, "End of life")
        self.assertEqual(self.product.product_state_id, self.state_end)
        self.assertEqual(self.product.product_state_history_count, 1)
        history = self.product.product_state_history_ids
        self.assertEqual(history.old_state_id, self.state_sellable)
        self.assertEqual(history.new_state_id, self.state_end)
        self.assertEqual(history.reason, "End of life")
        self.assertEqual(history.user_id, self.env.user)

    def test_user_cannot_unlink_history(self):
        self._change_state(self.product, self.state_end, "Keep this")
        history = self.product.product_state_history_ids
        user = self._create_internal_user("product_state_history_user")
        with self.assertRaises(AccessError):
            history.with_user(user).unlink()

    def test_user_without_group_cannot_open_change_wizard(self):
        user = self._create_internal_user("product_state_history_no_change")
        with self.assertRaises(AccessError):
            self.product.with_user(user).action_change_product_state()

    def test_user_with_group_can_change_state(self):
        user = self._create_internal_user(
            "product_state_history_change",
            groups=(
                self.env.ref("product.group_product_manager"),
                self.env.ref("product_state_history.group_product_state_change"),
            ),
        )
        self.product.with_user(user).action_change_product_state()
        self._change_state(
            self.product.with_user(user), self.state_end, "Allowed change"
        )
        self.assertEqual(self.product.product_state_id, self.state_end)
        self.assertEqual(
            self.product.product_state_history_ids.reason, "Allowed change"
        )
