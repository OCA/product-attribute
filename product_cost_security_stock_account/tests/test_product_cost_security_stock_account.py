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

    def _generate_and_validate_picking(
        self, product, picking_type=None, loc_orig=None, loc_dest=None
    ):
        picking_type = picking_type or self.stock_picking_type
        loc_orig = loc_orig or self.location_orig
        loc_dest = loc_dest or self.location_dest

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": picking_type.id,
                "location_id": loc_orig.id,
                "location_dest_id": loc_dest.id,
                "partner_id": self.partner.id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_uom_qty": 10,
                "product_uom": product.uom_id.id,
                "location_id": loc_orig.id,
                "location_dest_id": loc_dest.id,
                "product_id": product.id,
            }
        )
        # Odoo 19 Validation
        picking.action_confirm()
        move.picked = True

        # Validate picking to ensure that error is not thrown
        picking.button_validate()
        return picking, move

    @users("__system__", "user_test")
    def test_avco_picking_flow(self):
        picking, move = self._generate_and_validate_picking(self.product)
        # Odoo 19: stock.valuation.layer replaced by direct value on stock.move
        # unit_cost = move.value / move.quantity
        self.assertEqual(move.value / move.quantity, 5)

    @users("__system__", "user_test")
    def test_change_category(self):
        self._generate_and_validate_picking(self.product2)
        # Change category of product to avco to recompute the svls
        self.product2.categ_id = self.category1

    @users("__system__", "user_test")
    def test_outgoing_picking_flow(self):
        loc_customer = self.env["stock.location"].create(
            {"name": "Customer", "usage": "customer"}
        )
        picking_type_out = self.env["stock.picking.type"].create(
            {
                "name": "Test Out",
                "code": "outgoing",
                "sequence_id": self.sequence.id,
                "sequence_code": "test_out",
            }
        )

        # Update available quantity so we can deliver it
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.location_dest, 10.0
        )

        picking, move = self._generate_and_validate_picking(
            self.product,
            picking_type=picking_type_out,
            loc_orig=self.location_dest,
            loc_dest=loc_customer,
        )
        # Odoo 19: stock.valuation.layer replaced by is_valued field on stock.move
        self.assertTrue(move.is_valued)
