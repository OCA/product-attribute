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
    """consume_on_create and duplicate_check on, for gap-free sequences"""

    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.consume_on_create", "True"
        )
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.duplicate_check", "check"
        )

    def test_peek_does_not_consume(self):
        name = self.env["stock.lot"]._peek_next_name(self.product)
        self.assertEqual(name, "ABC0000101")
        self.assertEqual(self._next_number(), 101)
        self.assertEqual(
            self.env["stock.lot"]._peek_next_name(self.product), "ABC0000101"
        )
        self.assertEqual(self._next_number(), 101)

    def test_default_name_does_not_consume(self):
        self.assertEqual(self.env["stock.lot"]._default_name(), "ABC0000101")
        self.assertEqual(self._next_number(), 101)

    def test_mass_create_advances_past_whole_batch(self):
        names = [f"ABC{101 + index:07d}" for index in range(20)]
        lots = self._create_lots(names)
        self.assertEqual(lots.mapped("name"), names)
        self.assertEqual(self._next_number(), 121)

    def test_second_batch_does_not_collide(self):
        self._create_lots([f"ABC{101 + index:07d}" for index in range(20)])
        self.assertEqual(
            self.env["stock.lot"]._peek_next_name(self.product), "ABC0000121"
        )

    def test_create_without_name_consumes_one(self):
        lot = self.env["stock.lot"].create({"product_id": self.product.id})
        self.assertEqual(lot.name, "ABC0000101")
        self.assertEqual(self._next_number(), 102)

    def test_vendor_name_leaves_sequence_untouched(self):
        lots = self._create_lots(["VND-4711-1", "VND-4711-2"])
        self.assertEqual(lots.mapped("name"), ["VND-4711-1", "VND-4711-2"])
        self.assertEqual(self._next_number(), 101)

    def test_name_below_next_number_does_not_rewind(self):
        self._create_lots(["ABC0000150"])
        self.assertEqual(self._next_number(), 151)
        self._create_lots(["ABC0000120"])
        self.assertEqual(self._next_number(), 151)

    def test_duplicate_across_products_is_refused(self):
        self._create_lots(["ABC0000101"], product=self.other_product)
        with self.assertRaises(UserError):
            self._create_lots(["ABC0000101"])

    def test_duplicate_vendor_name_across_products_is_allowed(self):
        self._create_lots(["VND-4711-1"], product=self.other_product)
        lots = self._create_lots(["VND-4711-1"])
        self.assertEqual(lots.name, "VND-4711-1")

    def test_suffix_is_part_of_the_pattern(self):
        self.sequence.write({"prefix": "ABC", "suffix": "/X"})
        self._create_lots(["ABC0000150/X", "ABC0000160/Y"])
        self.assertEqual(self._next_number(), 151)

    def test_batch_keeps_digits_in_prefix_and_suffix(self):
        self.sequence.write({"prefix": "AB12", "suffix": "34CD"})
        names = self.env["stock.lot"].generate_lot_names("AB12000010134CD", 3)
        self.assertEqual(
            [name["lot_name"] for name in names],
            ["AB12000010134CD", "AB12000010234CD", "AB12000010334CD"],
        )

    def test_resync_with_digits_in_prefix_and_suffix(self):
        self.sequence.write({"prefix": "AB12", "suffix": "34CD"})
        self._create_lots(["AB12000010134CD", "AB12000010234CD", "AB12000010334CD"])
        self.assertEqual(self._next_number(), 104)

    def test_batch_advances_the_number_not_the_date(self):
        # digits on both sides of the number, as date placeholders render them
        self.sequence.write({"prefix": "ABC%(y)s", "suffix": "%(year)s-/X.Y"})
        seed = self.env["stock.lot"]._peek_next_name(self.product)
        names = self.env["stock.lot"].generate_lot_names(seed, 3)
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

    def test_year_placeholder_in_prefix(self):
        self.sequence.write({"prefix": "P%(year)s", "padding": 5})
        self.sequence.number_next_actual = 1
        self._create_lots(["P202600012"])
        self.assertEqual(self._next_number(), 13)

    def test_unsupported_placeholder_is_refused(self):
        self.sequence.write({"prefix": "P%(quarter)s"})
        with self.assertRaises(UserError):
            self._create_lots(["P10000012"])

    def test_other_year_still_matches_the_pattern(self):
        self.sequence.write({"prefix": "P%(year)s", "padding": 5})
        self.sequence.number_next_actual = 1
        self._create_lots(["P202000042"])
        self.assertEqual(self._next_number(), 43)

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
        self.assertEqual(self._next_number(), 101)


class TestLotSequenceDefaults(LotSequenceCase):
    """Default configurations"""

    def test_mass_create_still_advances_past_whole_batch(self):
        self._create_lots([f"ABC{101 + index:07d}" for index in range(20)])
        self.assertEqual(self._next_number(), 121)

    def test_admin_bypasses_the_duplicate_check(self):
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.duplicate_check", "admin"
        )
        self._create_lots(["ABC0000101"], product=self.other_product)
        lots = self._create_lots(["ABC0000101"])
        self.assertEqual(lots.name, "ABC0000101")

    def test_non_admin_is_refused_by_the_duplicate_check(self):
        self.env["ir.config_parameter"].set_param(
            "product_lot_sequence.duplicate_check", "admin"
        )
        self._create_lots(["ABC0000101"], product=self.other_product)
        stock_user = self.env["res.users"].create(
            {
                "name": "Stock user",
                "login": "lot_sequence_stock_user",
                "groups_id": [(6, 0, [self.env.ref("stock.group_stock_user").id])],
            }
        )
        with self.assertRaises(UserError):
            self.env["stock.lot"].with_user(stock_user).create(
                [{"name": "ABC0000101", "product_id": self.product.id}]
            )
