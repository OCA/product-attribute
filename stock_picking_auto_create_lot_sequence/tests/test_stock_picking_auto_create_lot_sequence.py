# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestStockPickingProductLotSequence(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier_location_id = cls.env.ref("stock.stock_location_suppliers").id
        cls.stock_location_id = cls.env.ref("stock.stock_location_stock").id
        cls.picking_type_in_id = cls.env.ref("stock.picking_type_in").id
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "tracking": "serial",
                "auto_create_lot": True,
            }
        )
        cls.product.lot_sequence_id.write(
            {
                "prefix": "Test/",
                "padding": 5,
                "number_increment": 1,
                "number_next_actual": 1,
            }
        )
        cls.picking = cls.env["stock.picking"].create(
            {
                "location_id": cls.supplier_location_id,
                "location_dest_id": cls.stock_location_id,
                "picking_type_id": cls.picking_type_in_id,
            }
        )
        cls.move = cls.env["stock.move"].create(
            {
                "name": "Test Move",
                "product_id": cls.product.id,
                "product_uom_qty": 10,
                "product_uom": cls.product.uom_id.id,
                "picking_id": cls.picking.id,
                "location_id": cls.supplier_location_id,
                "location_dest_id": cls.stock_location_id,
            }
        )

    def test_stock_picking_product_lot_sequence(self):
        self.picking.picking_type_id.auto_create_lot = True
        self.assertTrue(self.product.lot_sequence_id)
        next_serial = self.env["stock.lot"]._get_next_serial(
            self.env.company, self.product
        )
        self.assertRegex(next_serial, r"Test/\d{5}")
        self.picking.action_confirm()
        self.picking.action_assign()
        immediate_wizard = self.picking.button_validate()
        self.assertEqual(immediate_wizard.get("res_model"), "stock.immediate.transfer")
        immediate_wizard_form = Form(
            self.env[immediate_wizard["res_model"]].with_context(
                **immediate_wizard["context"]
            )
        ).save()
        immediate_wizard_form.process()
        for move_line in self.picking.move_line_ids:
            self.assertRegex(move_line.lot_name, r"Test/\d{5}")
