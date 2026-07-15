# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import new_test_user, users

from odoo.addons.base.tests.common import BaseCommon


class TestProductCostSecurityStockAccount(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_user = new_test_user(
            cls.env,
            login="user_test",
            groups="stock.group_stock_user",
        )
        cls.sequence = cls.env["ir.sequence"].create(
            {
                "name": "test seq",
                "implementation": "standard",
                "padding": 1,
                "number_increment": 1,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner test"})
        cls.category1 = cls.env["product.category"].create(
            {
                "name": "Test category 1",
                "property_cost_method": "average",
                "property_valuation": "real_time",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "type": "consu",
                "is_storable": True,
                "name": "Test product",
                "categ_id": cls.category1.id,
                "standard_price": 5,
            }
        )
        cls.location_dest = cls.env["stock.location"].create(
            {"name": "Test location dest", "usage": "internal"}
        )
        cls.location_orig = cls.env["stock.location"].create(
            {"name": "Test location orig", "usage": "supplier"}
        )
        cls.stock_picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Test picking type",
                "code": "incoming",
                "sequence_id": cls.sequence.id,
                "sequence_code": "test",
                "default_location_src_id": cls.location_orig.id,
                "default_location_dest_id": cls.location_dest.id,
            }
        )
        cls.category2 = cls.env["product.category"].create(
            {
                "name": "Test category 2",
                "property_cost_method": "standard",
            }
        )
        cls.product2 = cls.env["product.product"].create(
            {
                "type": "consu",
                "is_storable": True,
                "name": "Test product 2",
                "categ_id": cls.category2.id,
                "standard_price": 5,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product2, cls.location_dest, 5.0
        )

    def _generate_and_validate_picking(self, product):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.stock_picking_type.id,
                "location_id": self.location_orig.id,
                "location_dest_id": self.location_dest.id,
                "partner_id": self.partner.id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "name": "/",
                "picking_id": picking.id,
                "product_uom_qty": 10,
                "product_uom": product.uom_id.id,
                "location_id": self.location_orig.id,
                "location_dest_id": self.location_dest.id,
                "product_id": product.id,
            }
        )
        picking.button_validate()
        return picking, move

    def test_stock_user_can_create_product_without_cost_group(self):
        """Create storable product without cost ACL must not raise AccessError."""
        product_manager = new_test_user(
            self.env,
            login="user_product_no_cost",
            groups="stock.group_stock_user,product.group_product_manager",
        )
        template = (
            self.env["product.template"]
            .with_user(product_manager)
            .create(
                {
                    "name": "Product created without cost access",
                    "type": "consu",
                    "is_storable": True,
                    "categ_id": self.category2.id,
                }
            )
        )
        self.assertTrue(template.product_variant_ids)

    @users("__system__", "user_test")
    def test_avco_picking_flow(self):
        picking, move = self._generate_and_validate_picking(self.product)
        self.assertTrue(picking.state, "done")
        self.assertEqual(move.value, 50.0)

    @users("__system__", "user_test")
    def test_change_category(self):
        self._generate_and_validate_picking(self.product2)
        self.product2.categ_id = self.category1

    def test_stock_user_cannot_read_valuation_fields(self):
        with self.assertRaises(AccessError):
            self.product.with_user(self.stock_user).read(["avg_cost"])
        with self.assertRaises(AccessError):
            self.product.with_user(self.stock_user).read(["total_value"])

    def test_valuation_action_requires_cost_group(self):
        action = self.env.ref("stock_account.stock_move_valuation_action")
        self.assertIn(
            self.env.ref("product_cost_security.group_product_cost"),
            action.group_ids,
        )

    def test_stock_user_cannot_open_avco_report_action(self):
        with self.assertRaises(AccessError):
            self.env["ir.actions.actions"].with_user(self.stock_user)._for_xml_id(
                "stock_account.stock_avco_report_action"
            )

    def test_stock_user_cannot_open_valuation_action(self):
        with self.assertRaises(AccessError):
            self.env["ir.actions.actions"].with_user(self.stock_user)._for_xml_id(
                "stock_account.stock_move_valuation_action"
            )
