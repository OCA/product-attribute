# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestStockLotUniqueName(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = cls.env.ref("stock_lot_unique_name.group_allow_duplicate_lot_name")
        cls.product = cls.env["product.product"].create(
            {"name": "Tracked product", "tracking": "serial"}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Other tracked product", "tracking": "serial"}
        )
        cls.stock_groups = [
            cls.env.ref("base.group_user").id,
            cls.env.ref("stock.group_stock_user").id,
        ]
        cls.restricted_user = cls.env["res.users"].create(
            {
                "name": "Restricted user",
                "login": "lot_unique_restricted",
                "groups_id": [(6, 0, cls.stock_groups)],
            }
        )
        cls.allowed_user = cls.env["res.users"].create(
            {
                "name": "Allowed user",
                "login": "lot_unique_allowed",
                "groups_id": [(6, 0, cls.stock_groups + [cls.group.id])],
            }
        )

    def _create_lot(self, name, product=None, user=None):
        lot_model = self.env["stock.lot"]
        if user:
            lot_model = lot_model.with_user(user)
        return lot_model.create(
            {"name": name, "product_id": (product or self.product).id}
        )

    def test_a_user_created_later_is_not_granted_the_group(self):
        user = self.env["res.users"].create(
            {"name": "Later user", "login": "lot_unique_later"}
        )
        self.assertNotIn(self.group, user.groups_id)

    def test_group_member_may_reuse_a_name(self):
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000101", user=self.allowed_user)
        self.assertEqual(lot.name, "ABC0000101")

    def test_module_data_may_reuse_a_name(self):
        # odoo's own demo gives one serial to three products, so a module
        # declaring a duplicate must still install
        self._create_lot("ABC0000101", product=self.other_product)
        lot = (
            self.env["stock.lot"]
            .with_user(self.restricted_user)
            .with_context(install_module="mrp_workorder")
            .create({"name": "ABC0000101", "product_id": self.product.id})
        )
        self.assertEqual(lot.name, "ABC0000101")

    def test_duplicate_across_products_is_refused(self):
        self._create_lot("ABC0000101", product=self.other_product)
        with self.assertRaises(UserError):
            self._create_lot("ABC0000101", user=self.restricted_user)

    def test_same_name_on_the_same_product_is_left_to_odoo(self):
        self._create_lot("ABC0000101")
        # core's _check_unique_lot owns this case
        with self.assertRaises(ValidationError):
            self._create_lot("ABC0000101", user=self.restricted_user)

    def test_distinct_names_are_allowed(self):
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000102", user=self.restricted_user)
        self.assertEqual(lot.name, "ABC0000102")

    def test_batch_with_an_internal_duplicate_is_refused(self):
        with self.assertRaises(UserError):
            self.env["stock.lot"].with_user(self.restricted_user).create(
                [
                    {"name": "ABC0000101", "product_id": self.product.id},
                    {"name": "ABC0000101", "product_id": self.other_product.id},
                ]
            )

    def test_rename_onto_another_product_name_is_refused(self):
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000102", user=self.restricted_user)
        with self.assertRaises(UserError):
            lot.with_user(self.restricted_user).name = "ABC0000101"

    def test_rename_without_collision_is_allowed(self):
        lot = self._create_lot("ABC0000101", user=self.restricted_user)
        lot.with_user(self.restricted_user).name = "ABC0000102"
        self.assertEqual(lot.name, "ABC0000102")
