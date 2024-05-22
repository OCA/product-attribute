from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductLotSequence(TransactionCase):
    """Test product lot sequence."""

    def setUp(self):
        super(TestProductLotSequence, self).setUp()
        self.product_product = self.env["product.product"]
        self.stock_production_lot = self.env["stock.lot"]
        self.receipt_type = self.env.ref("stock.picking_type_in")
        self.delivery_type = self.env.ref("stock.picking_type_out")

    def _create_picking(self, picking_type, move_vals_list):
        picking_form = Form(self.env["stock.picking"])
        picking_form.picking_type_id = picking_type
        for move_vals in move_vals_list:
            with picking_form.move_ids_without_package.new() as move_form:
                move_form.product_id = move_vals.get("product_id")
                move_form.product_uom_qty = move_vals.get("product_uom_qty", 1.0)
                move_form.product_uom = move_vals.get(
                    "product_uom", self.env.ref("uom.product_uom_unit")
                )
        picking = picking_form.save()
        picking.action_confirm()
        return picking

    def test_product_sequence(self):
        self.assertEqual(self.stock_production_lot._get_sequence_policy(), "product")
        product = self.product_product.create(
            dict(name="The bar of foo", tracking="serial")
        )
        self.assertTrue(product.lot_sequence_id)
        product.lot_sequence_id.write(
            dict(
                prefix="foo/",
                padding=5,
                number_increment=1,
                number_next_actual=1,
                suffix="/bar",
            )
        )
        next_serial = self.env["stock.lot"]._get_next_serial(self.env.company, product)
        self.assertRegex(next_serial, r"foo/\d{5}/bar")

    def test_lot_onchange_product_id(self):
        self.assertEqual(self.stock_production_lot._get_sequence_policy(), "product")
        product = self.product_product.create(dict(name="Shiba plush", tracking="lot"))
        self.assertTrue(product.lot_sequence_id)
        product.lot_sequence_id.write(
            dict(prefix="shiba/", padding=4, number_increment=1, number_next_actual=1)
        )
        lot_form = Form(self.stock_production_lot)
        lot_form.product_id = product
        lot_form.company_id = self.env.company
        lot = lot_form.save()
        self.assertRegex(lot.name, r"shiba/\d{4}$")

    def test_global_sequence(self):
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.policy", "global"
        )
        product_1 = self.product_product.create(
            {"name": "Test global 1", "tracking": "serial"}
        )
        self.assertFalse(product_1.lot_sequence_id)
        product_2 = self.product_product.create(
            {"name": "Test global 2", "tracking": "lot"}
        )
        self.assertFalse(product_2.lot_sequence_id)
        seq = self.env["ir.sequence"].search([("code", "=", "stock.lot.serial")])
        next_sequence_number = seq.get_next_char(seq.number_next_actual)
        next_serial = self.env["stock.lot"]._get_next_serial(
            self.env.company, product_1
        )
        self.assertEqual(next_serial, next_sequence_number)
        seq._get_number_next_actual()
        next_sequence_number_2 = seq.get_next_char(seq.number_next_actual)
        next_serial_2 = self.env["stock.lot"]._get_next_serial(
            self.env.company, product_2
        )
        self.assertEqual(next_serial_2, next_sequence_number_2)

    def test_lot_onchange_product_id_global(self):
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.policy", "global"
        )
        product = self.product_product.create(
            {"name": "Test global", "tracking": "serial"}
        )
        self.assertFalse(product.lot_sequence_id)
        seq = self.env["ir.sequence"].search([("code", "=", "stock.lot.serial")])
        next_sequence_number = seq.get_next_char(seq.number_next_actual)
        lot_form = Form(
            self.stock_production_lot.with_context(
                default_company_id=self.env.company.id
            )
        )
        self.assertEqual(lot_form.name, next_sequence_number)
        self.assertEqual(lot_form.company_id, self.env.company)
        lot_form.product_id = product
        lot = lot_form.save()
        self.assertEqual(lot.name, next_sequence_number)

    def test_open_detailed_operations(self):
        # Required for `product_uom` to be visible in the view
        self.env.user.groups_id += self.env.ref("uom.group_uom")

        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.policy", "global"
        )
        seq = self.env["ir.sequence"].search([("code", "=", "stock.lot.serial")])
        first_next_sequence_number = seq.get_next_char(seq.number_next_actual)
        product = self.product_product.create(
            {"name": "Test global", "tracking": "serial"}
        )
        delivery_picking = self._create_picking(
            self.delivery_type, [{"product_id": product}]
        )
        delivery_move = delivery_picking.move_ids
        self.assertFalse(delivery_move.next_serial)
        delivery_move.action_show_details()
        self.assertFalse(delivery_move.next_serial)
        self.assertEqual(
            seq.get_next_char(seq.number_next_actual), first_next_sequence_number
        )
        receipt_picking = self._create_picking(
            self.receipt_type, [{"product_id": product}]
        )
        receipt_move = receipt_picking.move_ids
        self.assertFalse(receipt_move.next_serial)
        receipt_move.action_show_details()
        self.assertEqual(receipt_move.next_serial, first_next_sequence_number)
        new_next_sequence_number = seq.get_next_char(seq.number_next_actual)
        self.assertNotEqual(new_next_sequence_number, first_next_sequence_number)
        receipt_move.action_show_details()
        self.assertEqual(
            new_next_sequence_number, seq.get_next_char(seq.number_next_actual)
        )
