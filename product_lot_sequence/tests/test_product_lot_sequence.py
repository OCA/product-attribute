from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductLotSequence(TransactionCase):
    """Test product lot sequence."""

    def setUp(self):
        super(TestProductLotSequence, self).setUp()
        self.product_product = self.env["product.product"]
        self.stock_production_lot = self.env["stock.production.lot"]

    def test_product_sequence(self):
        product = self.product_product.create(
            dict(name="The bar of foo", tracking="serial")
        )
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
        product = self.product_product.create(dict(name="Shiba plush", tracking="lot"))
        product.lot_sequence_id.write(
            dict(prefix="shiba/", padding=4, number_increment=1, number_next_actual=1)
        )
        lot_form = Form(self.stock_production_lot)
        lot_form.product_id = product
        lot_form.company_id = self.env.company
        lot = lot_form.save()
        self.assertRegexpMatches(lot.name, r"shiba/\d{4}$")
