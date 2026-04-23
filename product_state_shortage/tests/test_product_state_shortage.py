# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestProductStateShortage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shortage_product_state = cls.env["product.state"].create(
            {
                "name": "Shortage",
                "code": "S",
                "is_shortage": True,
            }
        )
        cls.test_product_state = cls.env["product.state"].create(
            {
                "name": "Test",
                "code": "T",
                "is_shortage": False,
            }
        )
        cls.default_product_state = cls.env[
            "product.template"
        ]._get_default_product_state()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "product_state_id": cls.shortage_product_state.id,
                "detailed_type": "product",
            }
        )
        cls.wh = cls.env["stock.warehouse"].search([], limit=1)
        cls.loc_shelf_1 = cls.env["stock.location"].create(
            {"name": "Shelf 1", "location_id": cls.wh.lot_stock_id.id}
        )
        cls.loc_shelf_2 = cls.env["stock.location"].create(
            {"name": "Shelf 2", "location_id": cls.wh.lot_stock_id.id}
        )
        cls.loc_supplier = cls.env["stock.location"].search(
            [("usage", "=", "supplier")], limit=1
        )
        cls.loc_customer = cls.env["stock.location"].search(
            [("usage", "=", "customer")], limit=1
        )

    def _create_picking(self, pick_type, product, qty, loc_from, loc_to):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": pick_type.id,
                "move_ids": [
                    Command.create(
                        {
                            "name": f"{product.name}: {self.loc_supplier.name} "
                            f"-> {self.wh.wh_input_stock_loc_id.name}",
                            "product_id": product.id,
                            "product_uom_qty": qty,
                            "product_uom": self.product.uom_id.id,
                            "location_id": loc_from.id,
                            "location_dest_id": loc_to.id,
                        }
                    )
                ],
            }
        )
        return picking

    def _do_picking(self, picking):
        picking.action_confirm()
        picking.action_assign()
        picking.action_set_quantities_to_reservation()
        picking._action_done()

    def _do_reception_picking(self, product, qty=1):
        picking = self._create_picking(
            pick_type=self.wh.in_type_id,
            product=self.product,
            qty=qty,
            loc_from=self.loc_supplier,
            loc_to=self.wh.wh_input_stock_loc_id,
        )
        self._do_picking(picking)

    def test_receiving_new_stock_resets_shortage_state(self):
        self.assertEqual(self.product.product_state_id, self.shortage_product_state)
        self._do_reception_picking(self.product, qty=1)
        self.assertEqual(self.product.product_state_id, self.default_product_state)

    def test_only_incoming_transfers_reset_shortage_state(self):
        self.assertEqual(self.product.product_state_id, self.shortage_product_state)
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.loc_shelf_1, 15.0
        )

        # Internal should not reset "shortage"
        picking = self._create_picking(
            pick_type=self.wh.int_type_id,
            product=self.product,
            qty=5,
            loc_from=self.loc_shelf_1,
            loc_to=self.loc_shelf_2,
        )
        self._do_picking(picking)
        self.assertEqual(self.product.product_state_id, self.shortage_product_state)

        # Outgoing should not reset "shortage"
        picking = self._create_picking(
            pick_type=self.wh.out_type_id,
            product=self.product,
            qty=5,
            loc_from=self.loc_shelf_1,
            loc_to=self.loc_customer,
        )
        self._do_picking(picking)
        self.assertEqual(self.product.product_state_id, self.shortage_product_state)

    def test_no_reset_if_not_shortage_state(self):
        self.product.product_state_id = self.test_product_state
        self.assertFalse(self.product.product_state_id.is_shortage)
        self._do_reception_picking(self.product, qty=1)
        # No reset since the state is not a "shortage" state
        self.assertNotEqual(self.product.product_state_id, self.default_product_state)

        self.product.product_state_id = self.shortage_product_state
        self._do_reception_picking(self.product, qty=1)
        self.assertEqual(self.product.product_state_id, self.default_product_state)
