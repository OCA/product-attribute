# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from .common import TestCommon
from .utils import make_pkg_values


class TestCalc(TestCommon):
    def test_contained_mapping(self):
        self.assertEqual(
            self.product_a.packaging_contained_mapping,
            {
                str(self.pkg_pallet.id): [
                    make_pkg_values(self.product_a, self.pkg_big_box, qty=10)
                ],
                str(self.pkg_big_box.id): [
                    make_pkg_values(self.product_a, self.pkg_box, qty=4)
                ],
                str(self.pkg_box.id): [
                    make_pkg_values(self.product_a, self.uom_unit, qty=50)
                ],
            },
        )
        # Update pkg qty
        self.pkg_pallet.relative_factor = 4000
        self.assertEqual(
            self.product_a.packaging_contained_mapping,
            {
                str(self.pkg_pallet.id): [
                    make_pkg_values(self.product_a, self.pkg_big_box, qty=20)
                ],
                str(self.pkg_big_box.id): [
                    make_pkg_values(self.product_a, self.pkg_box, qty=4)
                ],
                str(self.pkg_box.id): [
                    make_pkg_values(self.product_a, self.uom_unit, qty=50)
                ],
            },
        )

    def test_calc_1(self):
        """Test easy behavior 1."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_pallet, qty=1),
            make_pkg_values(self.product_a, self.pkg_big_box, qty=3),
            make_pkg_values(self.product_a, self.pkg_box, qty=1),
            make_pkg_values(self.product_a, self.uom_unit, qty=5),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(2655), expected)

    def test_calc_2(self):
        """Test easy behavior 2."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_big_box, qty=1),
            make_pkg_values(self.product_a, self.pkg_box, qty=3),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(350), expected)

    def test_calc_3(self):
        """Test easy behavior 3."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_box, qty=1),
            make_pkg_values(self.product_a, self.uom_unit, qty=30),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(80), expected)

    def test_calc_6(self):
        """Test fractional qty is lost."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_box, qty=1),
            make_pkg_values(self.product_a, self.uom_unit, qty=0.5),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(50.5), expected)

    def test_calc_filter(self):
        """Test packaging filter."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_big_box, qty=13),
            make_pkg_values(self.product_a, self.pkg_box, qty=1),
            make_pkg_values(self.product_a, self.uom_unit, qty=5),
        ]
        self.assertEqual(
            self.product_a.with_context(
                _packaging_filter=lambda x: x != self.pkg_pallet
            ).product_qty_by_packaging(2655),
            expected,
        )

    def test_calc_name_get(self):
        """Test custom name getter."""
        expected = [
            make_pkg_values(
                self.product_a,
                self.pkg_pallet,
                qty=1,
                name="FOO " + self.pkg_pallet.name,
            ),
            make_pkg_values(
                self.product_a,
                self.pkg_big_box,
                qty=3,
                name="FOO " + self.pkg_big_box.name,
            ),
            make_pkg_values(
                self.product_a, self.pkg_box, qty=1, name="FOO " + self.pkg_box.name
            ),
            make_pkg_values(
                self.product_a, self.uom_unit, qty=5, name=self.uom_unit.name
            ),
        ]
        self.assertEqual(
            self.product_a.with_context(
                _packaging_name_getter=lambda x: "FOO " + x.name
            ).product_qty_by_packaging(2655),
            expected,
        )

    def test_calc_custom_values(self):
        """Test custom values handler."""
        expected = [
            {"my_qty": 1, "foo": self.pkg_pallet.name},
            {"my_qty": 3, "foo": self.pkg_big_box.name},
            {"my_qty": 1, "foo": self.pkg_box.name},
            {"my_qty": 5, "foo": self.uom_unit.name},
        ]
        self.assertEqual(
            self.product_a.with_context(
                _packaging_values_handler=lambda pkg, qty_per_pkg: {
                    "my_qty": qty_per_pkg,
                    "foo": pkg.name,
                }
            ).product_qty_by_packaging(2655),
            expected,
        )

    def test_calc_sub1(self):
        """Test contained packaging behavior 1."""
        expected = [
            make_pkg_values(
                self.product_a,
                self.pkg_pallet,
                qty=1,
                contained=[make_pkg_values(self.product_a, self.pkg_big_box, qty=10)],
            ),
            make_pkg_values(
                self.product_a,
                self.pkg_big_box,
                qty=3,
                contained=[make_pkg_values(self.product_a, self.pkg_box, qty=4)],
            ),
            make_pkg_values(
                self.product_a,
                self.pkg_box,
                qty=1,
                contained=[make_pkg_values(self.product_a, self.uom_unit, qty=50)],
            ),
            make_pkg_values(self.product_a, self.uom_unit, qty=5, contained=None),
        ]
        self.assertEqual(
            self.product_a.product_qty_by_packaging(2655, with_contained=True),
            expected,
        )

    def test_calc_sub2(self):
        """Test contained packaging behavior 2."""
        self.pkg_box.relative_factor = 30
        expected = [
            make_pkg_values(
                self.product_a,
                self.pkg_pallet,
                qty=1,
                contained=[make_pkg_values(self.product_a, self.pkg_big_box, qty=10)],
            ),
            make_pkg_values(
                self.product_a,
                self.pkg_big_box,
                qty=3,
                contained=[
                    make_pkg_values(self.product_a, self.pkg_box, qty=6),
                    make_pkg_values(self.product_a, self.uom_unit, qty=20),
                ],
            ),
            make_pkg_values(
                self.product_a,
                self.pkg_box,
                qty=1,
                contained=[make_pkg_values(self.product_a, self.uom_unit, qty=30)],
            ),
            make_pkg_values(self.product_a, self.uom_unit, qty=25, contained=None),
        ]
        self.assertEqual(
            self.product_a.product_qty_by_packaging(2655, with_contained=True),
            expected,
        )

    def test_calc_variant_packaging(self):
        """Test variant-specific packagings are considered."""
        crate = self.env["uom.uom"].create(
            {
                "name": "Crate",
                "relative_uom_id": self.uom_unit.id,
                "relative_factor": 1000,
            }
        )
        self.product_a.extra_uom_ids = [(4, crate.id)]
        expected = [
            make_pkg_values(self.product_a, crate, qty=1),
            make_pkg_values(self.product_a, self.pkg_big_box, qty=2),
            make_pkg_values(self.product_a, self.pkg_box, qty=2),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(1500), expected)

    def test_calc_product_uom_not_reference(self):
        """Test product UoM which is not a reference unit (e.g. Dozens)."""
        uom_dozen = self.env.ref("uom.product_uom_dozen")
        pkg_case = self.env["uom.uom"].create(
            {
                "name": "Case",
                "relative_uom_id": uom_dozen.id,
                "relative_factor": 20,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Product B",
                "uom_id": uom_dozen.id,
                "uom_ids": [(4, pkg_case.id)],
            }
        )
        expected = [
            make_pkg_values(product, pkg_case, qty=1),
            make_pkg_values(product, uom_dozen, qty=15),
        ]
        self.assertEqual(product.product_qty_by_packaging(35), expected)

    def test_calc_ignored_packaging(self):
        """Test product UoM and packagings smaller than it are ignored."""
        expected = [
            make_pkg_values(self.product_a, self.pkg_pallet, qty=1),
            make_pkg_values(self.product_a, self.pkg_big_box, qty=3),
            make_pkg_values(self.product_a, self.pkg_box, qty=1),
            make_pkg_values(self.product_a, self.uom_unit, qty=5),
        ]
        half = self.env["uom.uom"].create(
            {
                "name": "Half",
                "relative_uom_id": self.uom_unit.id,
                "relative_factor": 0.5,
            }
        )
        for uom in (self.uom_unit, half):
            with self.subTest(uom=uom.name):
                self.product_a.uom_ids = [(4, uom.id)]
                self.assertEqual(
                    self.product_a.product_qty_by_packaging(2655), expected
                )
                self.assertEqual(
                    self.product_a.product_qty_by_packaging_as_str(
                        10, only_packaging=True
                    ),
                    "",
                )

    def test_packaging_barcode_company(self):
        """Test barcode of the current company prevails over shared ones."""
        company_2 = self.env["res.company"].create({"name": "Company 2"})
        product_uom = self.env["product.uom"]
        product_uom.create(
            {
                "product_id": self.product_a.id,
                "uom_id": self.pkg_box.id,
                "barcode": "BOX-C2",
                "company_id": company_2.id,
            }
        )
        shared = product_uom.create(
            {
                "product_id": self.product_a.id,
                "uom_id": self.pkg_pallet.id,
                "barcode": "PALLET-SHARED",
                "company_id": False,
            }
        )
        product = self.product_a
        product_2 = self.product_a.with_company(company_2)
        self.assertEqual(product._packaging_barcode(self.pkg_box), "BOX")
        self.assertEqual(product_2._packaging_barcode(self.pkg_box), "BOX-C2")
        self.assertEqual(product._packaging_barcode(self.pkg_pallet), "PALLET")
        self.assertEqual(product_2._packaging_barcode(self.pkg_pallet), shared.barcode)
        self.assertIsNone(product_2._packaging_barcode(self.pkg_big_box))
        self.assertEqual(
            product_2.packaging_contained_mapping[str(self.pkg_big_box.id)][0][
                "barcode"
            ],
            "BOX-C2",
        )
