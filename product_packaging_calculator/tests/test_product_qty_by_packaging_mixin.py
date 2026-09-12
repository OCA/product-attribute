# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.orm.model_classes import add_to_registry

from .common import TestCommon


class TestPQPackagingMixin(TestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model natively (odoo_test_helper is not needed on Odoo 19+)
        from .models import TestProductQtyByPackagingMixin

        model_name = TestProductQtyByPackagingMixin._name
        add_to_registry(cls.registry, TestProductQtyByPackagingMixin)
        cls.addClassCleanup(cls.registry.__delitem__, model_name)
        cls.registry._setup_models__(cls.env.cr, [model_name])
        cls.registry.init_models(cls.env.cr, [model_name], {"models_to_check": True})
        cls.model = cls.env[model_name]

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
