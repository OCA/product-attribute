# Copyright 2021 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo.addons.product_packaging_calculator.tests.common import TestCommon
from odoo.addons.product_packaging_calculator.tests.utils import make_pkg_values


class TestCalc(TestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.level_retail_box = cls.env["product.packaging.level"].create(
            {"name": "Retail Box", "code": "PACK", "sequence": 3}
        )
        cls.level_transport_box = cls.env["product.packaging.level"].create(
            {"name": "Transport Box", "code": "CASE", "sequence": 4}
        )
        cls.level_pallet = cls.env["product.packaging.level"].create(
            {"name": "Pallet", "code": "PALLET", "sequence": 5}
        )
        cls.pkg_box.uom_id.packaging_level_id = cls.level_retail_box
        cls.pkg_big_box.uom_id.packaging_level_id = cls.level_transport_box
        cls.pkg_pallet.uom_id.packaging_level_id = cls.level_pallet

    def test_calc_1(self):
        expected = [
            make_pkg_values(self.pkg_pallet, qty=1, name=self.level_pallet.name),
            make_pkg_values(
                self.pkg_big_box, qty=3, name=self.level_transport_box.name
            ),
            make_pkg_values(self.pkg_box, qty=1, name=self.level_retail_box.name),
            make_pkg_values(self.uom_unit, qty=5),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(2655), expected)

    def test_calc_2(self):
        expected = [
            make_pkg_values(
                self.pkg_big_box, qty=1, name=self.level_transport_box.name
            ),
            make_pkg_values(self.pkg_box, qty=3, name=self.level_retail_box.name),
        ]
        self.assertEqual(self.product_a.product_qty_by_packaging(350), expected)

    def test_as_str(self):
        self.assertEqual(self.product_a.product_qty_by_packaging_as_str(10), "10 Units")
        self.assertEqual(self.product_a.product_qty_by_packaging_as_str(100), "2PACK")
        self.assertEqual(
            self.product_a.product_qty_by_packaging_as_str(250), "1CASE,\xa01PACK"
        )
        self.assertEqual(
            self.product_a.with_context(
                qty_by_packaging_level_fname="name",
                qty_by_packaging_level_compact=False,
            ).product_qty_by_packaging_as_str(250),
            "1 Transport Box,\xa01 Retail Box",
        )

    def test_fallback_and_mixin(self):
        # 1. Trigger the mixin compute method on empty recordset to cover it safely
        self.env[
            "product.qty_by_packaging.mixin"
        ]._compute_product_qty_by_packaging_display()

        # 2. Test _packaging_name_getter fallback (no level, and False)
        temp_uom = self.env["uom.uom"].create(
            {
                "name": "Temp UoM",
                "relative_uom_id": self.uom_unit.id,
                "relative_factor": 10.0,
                "packaging_level_id": False,
            }
        )
        temp_pkg = self.env["product.uom"].create(
            {
                "product_id": self.product_a.id,
                "uom_id": temp_uom.id,
                "barcode": "TEMPPKG",
            }
        )
        self.assertEqual(self.product_a._packaging_name_getter(temp_pkg), "Temp UoM")
        self.assertEqual(self.product_a._packaging_name_getter(False), False)

        # 3. Test _qty_by_packaging_as_str fallback (no level, and False)
        self.assertEqual(
            self.product_a._qty_by_packaging_as_str(temp_pkg, 5), "5 Temp UoM"
        )
        self.assertEqual(self.product_a._qty_by_packaging_as_str(False, 5), False)
