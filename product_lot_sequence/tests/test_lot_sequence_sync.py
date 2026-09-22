# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class LotSequenceCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].set_param(
            "product_lot_sequence.policy", "global"
        )
        cls.sequence = cls.env["ir.sequence"].search(
            [("code", "=", "stock.lot.serial")], limit=1
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Sequenced product", "tracking": "serial"}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Other sequenced product", "tracking": "serial"}
        )
        cls.receipt_type = cls.env.ref("stock.picking_type_in")

    def setUp(self):
        super().setUp()
        self.sequence.write({"prefix": "ABC", "suffix": "", "padding": 7})
        self.sequence.number_next_actual = 101

    def _next_number(self):
        self.sequence.invalidate_recordset(["number_next_actual"])
        return self.sequence.number_next_actual

    def _create_lots(self, names, product=None):
        return self.env["stock.lot"].create(
            [
                {"name": name, "product_id": (product or self.product).id}
                for name in names
            ]
        )


class TestLotSequenceSync(LotSequenceCase):
    def test_mass_create_advances_past_whole_batch(self):
        names = [f"ABC{101 + index:07d}" for index in range(20)]
        lots = self._create_lots(names)
        self.assertEqual(lots.mapped("name"), names)
        self.assertEqual(self._next_number(), 121)

    def test_vendor_name_leaves_sequence_untouched(self):
        lots = self._create_lots(["VND-4711-1", "VND-4711-2"])
        self.assertEqual(lots.mapped("name"), ["VND-4711-1", "VND-4711-2"])
        self.assertEqual(self._next_number(), 101)

    def test_name_below_next_number_does_not_rewind(self):
        self._create_lots(["ABC0000150"])
        self.assertEqual(self._next_number(), 151)
        self._create_lots(["ABC0000120"])
        self.assertEqual(self._next_number(), 151)

    def test_suffix_is_part_of_the_pattern(self):
        self.sequence.write({"prefix": "ABC", "suffix": "/X"})
        self._create_lots(["ABC0000150/X", "ABC0000160/Y"])
        self.assertEqual(self._next_number(), 151)

    def test_resync_with_digits_in_prefix_and_suffix(self):
        self.sequence.write({"prefix": "AB12", "suffix": "34CD"})
        self._create_lots(["AB12000010134CD", "AB12000010234CD", "AB12000010334CD"])
        self.assertEqual(self._next_number(), 104)

    def test_year_placeholder_in_prefix(self):
        self.sequence.write({"prefix": "P%(year)s", "padding": 5})
        self.sequence.number_next_actual = 1
        self._create_lots(["P202600012"])
        self.assertEqual(self._next_number(), 13)

    def test_other_year_still_matches_the_pattern(self):
        self.sequence.write({"prefix": "P%(year)s", "padding": 5})
        self.sequence.number_next_actual = 1
        self._create_lots(["P202000042"])
        self.assertEqual(self._next_number(), 43)

    def test_batch_keeps_digits_in_prefix_and_suffix(self):
        self.sequence.write({"prefix": "AB12", "suffix": "34CD"})
        names = self.env["stock.lot"].generate_lot_names("AB12000010134CD", 3)
        self.assertEqual(
            [name["lot_name"] for name in names],
            ["AB12000010134CD", "AB12000010234CD", "AB12000010334CD"],
        )

    def test_batch_advances_the_number_not_the_date(self):
        # digits on both sides of the number, as date placeholders render them
        self.sequence.write({"prefix": "ABC%(y)s", "suffix": "%(year)s-/X.Y"})
        names = self.env["stock.lot"].generate_lot_names(
            self.sequence._lot_name_for(101), 3
        )
        regex = self.sequence._lot_name_regex()
        self.assertEqual(
            [int(regex.match(name["lot_name"]).group(1)) for name in names],
            [101, 102, 103],
        )

    def test_unknown_name_falls_back_to_core(self):
        names = self.env["stock.lot"].generate_lot_names("VND-4711-8", 3)
        self.assertEqual(
            [name["lot_name"] for name in names],
            ["VND-4711-8", "VND-4711-9", "VND-4711-10"],
        )

    def test_unsupported_placeholder_is_refused(self):
        self.sequence.write({"prefix": "P%(quarter)s"})
        with self.assertRaises(UserError):
            self.env["stock.lot"].generate_lot_names("P10000012", 1)

    def test_generate_dialog_starts_at_the_sequence(self):
        vals_list = self.env["stock.move"].action_generate_lot_line_vals(
            {
                "default_product_id": self.product.id,
                "default_location_id": self.receipt_type.default_location_src_id.id,
                "default_location_dest_id": (
                    self.receipt_type.default_location_dest_id.id
                ),
                "default_tracking": "serial",
                "default_quantity": 3,
            },
            "generate",
            "",
            3,
            "",
        )
        self.assertEqual(
            [vals["lot_name"] for vals in vals_list],
            ["ABC0000101", "ABC0000102", "ABC0000103"],
        )
        # seeding the dialog takes one number from the sequence
        self.assertEqual(self._next_number(), 102)


class TestLotSequencePerProduct(LotSequenceCase):
    """Per-product policy, where several templates may share one sequence"""

    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.policy", "product"
        )
        self.product.product_tmpl_id.lot_sequence_id = self.sequence
        self.other_product.product_tmpl_id.lot_sequence_id = self.sequence

    def test_shared_sequence_sees_every_template(self):
        self.env["stock.lot"].create(
            [
                {"name": "ABC0000101", "product_id": self.product.id},
                {"name": "ABC0000150", "product_id": self.other_product.id},
            ]
        )
        # the highest name belongs to the second template, so grouping must not
        # drop it when both templates point at the same sequence
        self.assertEqual(self._next_number(), 151)
