# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo_test_helper import FakeModelLoader

from .common import TestCommon


class TestPQPackagingMixin(TestCommon):
    def setUp(self):
        super().setUp()
        # Load a test model using odoo_test_helper
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .models import TestProductQtyByPackagingMixin

        self.loader.update_registry((TestProductQtyByPackagingMixin,))
        self.model = self.env[TestProductQtyByPackagingMixin._name]

    def tearDown(self):
        self.loader.restore_registry()
        return super().tearDown()

    def test_1_quantity_packaging(self):
        record = self.model.create({"product_id": self.product_a.id, "quantity": 10})
        self.assertEqual(record.product_qty_by_packaging_display, "10 Units")
        self.assertEqual(
            record.with_context(
                qty_by_pkg_only_packaging=True
            ).product_qty_by_packaging_display,
            "",
        )
        record.quantity = 100
        self.assertEqual(record.product_qty_by_packaging_display, "2 Box")
        record.quantity = 250
        self.assertEqual(record.product_qty_by_packaging_display, "1 Big Box,\xa01 Box")
        record.quantity = 255
        self.assertEqual(
            record.product_qty_by_packaging_display,
            "1 Big Box,\xa01 Box,\xa05 Units",
        )
        # only_packaging has no impact if we get not only units
        self.assertEqual(
            record.with_context(
                qty_by_pkg_only_packaging=True
            ).product_qty_by_packaging_display,
            "1 Big Box,\xa01 Box,\xa05 Units",
        )

    def test_2_fractional_quantity(self):
        record = self.model.create(
            {"product_id": self.product_a.id, "quantity": 100.45}
        )
        self.assertEqual(
            record.product_qty_by_packaging_display, "2 Box,\xa00.45 Units"
        )
