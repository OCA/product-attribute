from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import SavepointCase
from odoo.tools.float_utils import float_compare


@tagged("post_install", "-at_install")
class TestUomConverter(SavepointCase):
    # would be nice to use https://pypi.org/project/parameterized/

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.egg_flow = cls.env["uom.converter"].create(
            dict(
                name="Average egg laying per day - Dozen to Days",
                from_uom_id=cls.env.ref("uom.product_uom_dozen").id,
                to_uom_id=cls.env.ref("uom.product_uom_day").id,
                line_ids=[
                    (
                        0,
                        0,
                        {
                            "max_qty": 10,
                            "coefficient": 0.5,
                            "constant": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            # do not create lines in the expected sorted order
                            "max_qty": 1,
                            "coefficient": 0,
                            "constant": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "max_qty": 100,
                            "coefficient": 0.3,
                            "constant": 5,
                        },
                    ),
                ],
            )
        )
        cls.midas = cls.env["uom.converter"].create(
            dict(
                name="Water to Gold by king Midas - L to Kg",
                from_uom_id=cls.env.ref("uom.product_uom_litre").id,
                to_uom_id=cls.env.ref("uom.product_uom_kgm").id,
                line_ids=[
                    (
                        0,
                        0,
                        {
                            "max_qty": 3,
                            "coefficient": 10,
                            "constant": 0.5,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "max_qty": 9,
                            "coefficient": 20,
                            "constant": 2.3,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "max_qty": 20,
                            "coefficient": 50,
                            "constant": 4.2,
                        },
                    ),
                ],
            )
        )

    def test_default_params(self):
        values = [
            [0, 1, "test-0"],
            [2, 1 + 0.5 * 2, "test-2"],
            [3, 1 + 0.5 * 3, "test-3"],
            [10, 1 + 0.5 * 10, "test-10"],
            [10.1, 5 + 10.1 * 0.3, "test-10.1"],
            [100, 5 + 100 * 0.3, "test-100"],
        ]
        for qty, expected, id_test in values:
            result = self.egg_flow.convert(qty)
            self.assertEqual(
                float_compare(
                    result,
                    expected,
                    precision_rounding=self.egg_flow.to_uom_id.rounding,
                ),
                0,
                msg=f"{id_test}: Converted qty ({result}) "
                f"!= expected qty ({expected})",
            )

    def test_change_input_uom_qty(self):
        result = self.egg_flow.convert(
            3 * 12,
            uom_qty=self.env.ref("uom.product_uom_unit"),
        )
        expected = 1 + 0.5 * 3
        self.assertEqual(
            float_compare(
                result,
                expected,
                precision_rounding=self.egg_flow.to_uom_id.rounding,
            ),
            0,
            msg=f"testing change_input_uom_qty: Converted qty ({result}) "
            f"!= expected qty ({expected})",
        )

    def test_change_input_uom_qty_and_result_uom(self):
        to_uom = self.env.ref("uom.product_uom_hour")
        result = self.egg_flow.convert(
            99 * 12,
            uom_qty=self.env.ref("uom.product_uom_unit"),
            result_uom=to_uom,
        )
        # As uom module hour in work time 1 day is 8.0 hours
        expected = (5 + 0.3 * 99) * 8.0
        self.assertEqual(
            float_compare(
                result,
                expected,
                precision_rounding=to_uom.rounding,
            ),
            0,
            msg=f"testing change_input_uom_qty: Converted qty ({result}) "
            f"!= expected qty ({expected})",
        )

    def test_change_input_result_uom(self):
        to_uom = self.env.ref("uom.product_uom_hour")
        result = self.egg_flow.convert(
            99,
            result_uom=to_uom,
        )
        # As uom module hour in work time 1 day is 8.0 hours
        expected = (5 + 0.3 * 99) * 8.0
        self.assertEqual(
            float_compare(
                result,
                expected,
                precision_rounding=to_uom.rounding,
            ),
            0,
            msg=f"testing change_input_uom_qty: Converted qty ({result}) "
            f"!= expected qty ({expected})",
        )

    def test_wrong_uom_qty(self):
        with self.assertRaisesRegex(
            ValidationError,
            r"You can't convert Dozens \(expected Volume uom category\) to kg "
            "using this converter Water to Gold by king Midas - L to Kg.",
        ):
            self.midas.convert(1, uom_qty=self.env.ref("uom.product_uom_dozen"))

    def test_wrong_result_uom(self):
        with self.assertRaisesRegex(
            ValidationError,
            r"You can't convert L to Dozens \(expect Weight unit category\) "
            "using this converter Water to Gold by king Midas - L to Kg.",
        ):
            self.midas.convert(1, result_uom=self.env.ref("uom.product_uom_dozen"))

    def test_out_of_scale(self):
        with self.assertRaisesRegex(
            ValidationError,
            "You can't converter 20.1 L to kg using "
            "this converter Water to Gold by king Midas - L to Kg. "
            "This quantity is out of configured scale.",
        ):
            self.midas.convert(20.1)
