from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestProductLotSequence(SavepointCase):
    """Test product lot sequence."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.product_product = cls.env["product.product"]
        cls.stock_production_lot = cls.env["stock.production.lot"]
        cls.Settings = cls.env["res.config.settings"]
        cls.sequence = cls.env["ir.sequence"].search([], limit=1)

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
        self.assertRegexpMatches(product.lot_sequence_id._next(), r"foo/\d{5}/bar")

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

    def test_default_lot_sequence_set(self):
        """Check setting default lot sequence for a product"""

        # Create a configuration with a specified lot sequence ID
        config = self.Settings.create(
            {
                "lot_sequence_id": self.sequence.id,
            }
        )
        config.execute()

        # Create a product with a name and tracking set to "lot"
        product = self.product_product.create(
            {"name": "Default lot sequence product", "tracking": "lot"}
        )

        self.assertEqual(
            product.lot_sequence_id.id,
            self.sequence.id,
            msg="Must be equal default lot sequence ID #{sequence}".format(
                sequence=self.sequence.id
            ),
        )

    def test_copy_lot_sequence(self):
        """Check if copying a product copies the lot sequence of the copied product"""

        # Create a sequence for testing
        test_sequence = self.env["ir.sequence"].create(
            {
                "name": "Test Lot Sequence",
                "implementation": "no_gap",
                "prefix": "test/",
                "padding": 6,
                "number_increment": 1,
                "use_date_range": False,
            }
        )

        # Create a product with lot tracking and assign the test sequence
        original_product = self.product_product.create(
            {
                "name": "Original Product",
                "tracking": "lot",
                "lot_sequence_id": test_sequence.id,
            }
        )

        # Duplicate the product
        copied_product = original_product.product_tmpl_id.copy()

        # Check if the copied product retains the same sequence
        self.assertEqual(
            copied_product.lot_sequence_id.id,
            original_product.lot_sequence_id.id,
            msg="The copied product should retain the same"
            " lot sequence as the original product.",
        )
