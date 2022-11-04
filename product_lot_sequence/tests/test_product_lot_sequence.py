from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductLotSequence(TransactionCase):
    """Test product lot sequence."""

    def setUp(self):
        super(TestProductLotSequence, self).setUp()
        self.product_product = self.env["product.product"]
        self.stock_production_lot = self.env["stock.production.lot"]

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
        next_serial = self.env["stock.production.lot"]._get_next_serial(
            self.env.company, product
        )
        self.assertRegexpMatches(next_serial, r"foo/\d{5}/bar")

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
        self.assertRegexpMatches(lot.name, r"shiba/\d{4}$")

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
        next_serial = self.env["stock.production.lot"]._get_next_serial(
            self.env.company, product_1
        )
        self.assertEqual(next_serial, next_sequence_number)
        seq._get_number_next_actual()
        next_sequence_number_2 = seq.get_next_char(seq.number_next_actual)
        next_serial_2 = self.env["stock.production.lot"]._get_next_serial(
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
