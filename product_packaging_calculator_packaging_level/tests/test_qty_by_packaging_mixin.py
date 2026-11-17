# Copyright 2026 Foodles
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo_test_helper import FakeModelLoader

from odoo.addons.stock_packaging_calculator.tests.common import TestCommon


class TestQtyByPackagingMixinLevel(TestCommon):
    """Exercise the override of _compute_product_qty_by_packaging_display.

    The override only adds depends_context keys; we verify the field recomputes
    when those context keys change.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import TestProductQtyByPackagingMixinLevel

        cls.loader.update_registry((TestProductQtyByPackagingMixinLevel,))
        cls.model = cls.env[TestProductQtyByPackagingMixinLevel._name]

        cls.level_retail_box = cls.env["product.packaging.level"].create(
            {"name": "Retail Box", "code": "PACK", "sequence": 3}
        )
        cls.level_transport_box = cls.env["product.packaging.level"].create(
            {"name": "Transport Box", "code": "CASE", "sequence": 4}
        )
        cls.pkg_box.packaging_level_id = cls.level_retail_box
        cls.pkg_big_box.packaging_level_id = cls.level_transport_box

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_display_uses_level_code_by_default(self):
        record = self.model.create({"product_id": self.product_a.id, "quantity": 250})
        # Default: compact=True, fname="code"
        self.assertEqual(record.product_qty_by_packaging_display, "1CASE,\xa01PACK")

    def test_display_recomputes_on_context_change(self):
        record = self.model.create({"product_id": self.product_a.id, "quantity": 250})
        # Switch to non-compact + name -> the field must recompute thanks to
        # the depends_context added by this module.
        self.assertEqual(
            record.with_context(
                qty_by_packaging_level_fname="name",
                qty_by_packaging_level_compact=False,
            ).product_qty_by_packaging_display,
            "1 Transport Box,\xa01 Retail Box",
        )
        # And switch back: same record, different context => different value
        self.assertEqual(
            record.with_context(
                qty_by_packaging_level_fname="code",
                qty_by_packaging_level_compact=True,
            ).product_qty_by_packaging_display,
            "1CASE,\xa01PACK",
        )
