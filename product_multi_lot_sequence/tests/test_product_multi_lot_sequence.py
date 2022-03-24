from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductMultiLotSequence(TransactionCase):
    """Test product multi lot sequence."""

    def setUp(self):
        super(TestProductMultiLotSequence, self).setUp()
        self.product_product = self.env["product.product"]
        self.product_template = self.env["product.template"]
        self.stock_production_lot = self.env["stock.production.lot"]
        self.product_lot_sequence = self.env["product.lot.sequence"]

        self.product_unique_serial = self.product_product.create(
            dict(name="Product Unique Serial", tracking="serial")
        )
        self.product_lot_sequence_unique_serial = self.product_lot_sequence.create(
            dict(
                name="Product Unique Serial Sequence",
                lot_sequence_prefix="foo/",
                lot_sequence_padding=5,
                lot_sequence_suffix="/bar",
                lot_sequence_number_next=1000,
                product_id=self.product_unique_serial.id,
            )
        )
        self.product_unique_serial.update(
            dict(product_lot_sequence_ids=self.product_lot_sequence_unique_serial.ids)
        )

        self.product_lot_sequence_template_serial = self.product_lot_sequence.create(
            dict(
                name="Product Template Serial Sequence",
                lot_sequence_prefix="bar/",
                lot_sequence_padding=5,
                lot_sequence_suffix="/foo",
                lot_sequence_number_next=1000,
            )
        )
        self.product_product_serial = self.product_product.create(
            dict(
                name="Product Template Serial",
                tracking="serial",
                product_lot_sequence_ids=self.product_lot_sequence_template_serial.ids,
            )
        )

    def test_lot_creation_product_unique_serial(self):
        lot = self.stock_production_lot.create(
            dict(
                product_id=self.product_unique_serial.id, company_id=self.env.company.id
            )
        )
        lot.onchange_available_product_lot_sequence_ids()
        lot.onchange_product_lot_sequence_id()
        lot_form = Form(lot)
        lot = lot_form.save()
        self.assertRegexpMatches(lot.name, r"foo/\d{5}/bar")

    def test_lot_creation_product_template_serial(self):
        lot = self.stock_production_lot.create(
            dict(
                product_id=self.product_product_serial.id,
                company_id=self.env.company.id,
                product_lot_sequence_id=self.product_lot_sequence_template_serial.id,
            )
        )
        lot.onchange_product_lot_sequence_id()
        lot_form = Form(lot)
        lot = lot_form.save()
        self.assertRegexpMatches(lot.name, r"bar/\d{5}/foo")
