# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import new_test_user, users

from odoo.addons.base.tests.common import BaseCommon


class TestProductCostSecurityStockAccount(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uid = new_test_user(
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
                "product_uom": self.product.uom_id.id,
                "location_id": self.location_orig.id,
                "location_dest_id": self.location_dest.id,
                "product_id": product.id,
            }
        )
        # Validate picking to ensure that error is not thrown
        picking.button_validate()
        return picking, move

    @users("__system__", "user_test")
    def test_avco_picking_flow(self):
        picking, move = self._generate_and_validate_picking(self.product)
        self.assertEqual(move.stock_valuation_layer_ids.unit_cost, 5)

    @users("__system__", "user_test")
    def test_change_category(self):
        self._generate_and_validate_picking(self.product2)
        # Change category of product to avco to recompute the svls
        self.product2.categ_id = self.category1
