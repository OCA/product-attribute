# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.tests.common import TransactionCase


class TestProductMassAddition(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup Fake Models
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models.order import ModelOrder, ModelOrderLine

        cls.loader.update_registry((ModelOrder, ModelOrderLine))

        # Setup data
        cls.order = cls.env["model.order"].create({})
        cls.quick_ctx = dict(parent_model=cls.order._name, parent_id=cls.order.id)
        cls.product = cls.env.ref("product.product_product_8").with_context(
            **cls.quick_ctx
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_quick_line_add(self):
        """Test quick lines are added, updated and removed"""
        # Case 1: Create new line
        self.assertFalse(self.order.line_ids)
        self.product.qty_to_process = 5.0
        self.assertEqual(len(self.order.line_ids), 1, "A new line should be created")
        self.assertAlmostEqual(self.order.line_ids.product_qty, 5.0)
        # Case 2: Update existing line
        self.product.qty_to_process = 2.0
        self.assertEqual(len(self.order.line_ids), 1)
        self.assertAlmostEqual(self.order.line_ids.product_qty, 2.0)
        # Case 3: Set to 0 should remove the line
        self.product.qty_to_process = 0.0
        self.assertFalse(self.order.line_ids)

    def test_quick_should_not_write_on_product(self):
        """Using quick magic fields shouldn't write on product's metadata"""
        user_demo = self.env.ref("base.user_demo")
        self.product.write_uid = user_demo
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, user_demo)
        # Case 1: Updating qty_to_process shouldn't write on products
        self.product.qty_to_process = 1.0
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, user_demo)
        # Case 2: Updating quick_uom_id shouldn't write on products
        self.product.quick_uom_id = self.env.ref("uom.product_uom_categ_unit").uom_ids[
            1
        ]
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, user_demo)

    def test_quick_should_write_on_product(self):
        """Updating fields that are not magic fields should update
        product metadata"""
        # Change the product write_uid for testing
        user_demo = self.env.ref("base.user_demo")
        self.product.write_uid = user_demo
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, user_demo)
        # Case 1: Updating name field should write on product's metadata
        self.product.name = "Testing"
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, self.env.user)
        # Change the product write_uid for testing
        user_demo = self.env.ref("base.user_demo")
        self.product.write_uid = user_demo
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, user_demo)
        # Case 2: Updating qty_to_process and name before flush should
        # write on product's metadata
        self.product.qty_to_process = 2.0
        self.product.name = "Testing 2"
        self.env["base"].flush()
        self.assertEqual(self.product.write_uid, self.env.user)
