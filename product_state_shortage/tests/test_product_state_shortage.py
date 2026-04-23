# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductStateShortage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shortage_product_state = cls.env["product.state"].create(
            {
                "name": "Shortage",
                "code": "S",
                "is_shortage": True,
            }
        )
        cls.test_product_state = cls.env["product.state"].create(
            {
                "name": "Test",
                "code": "T",
                "is_shortage": False,
            }
        )
        cls.default_product_state = cls.env[
            "product.template"
        ]._get_default_product_state()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "product_state_id": cls.shortage_product_state.id,
                "detailed_type": "product",
            }
        )
        cls.wh = cls.env["stock.warehouse"].search([], limit=1)
        cls.loc_shelf_1 = cls.env["stock.location"].create(
            {"name": "Shelf 1", "location_id": cls.wh.lot_stock_id.id}
        )

    def test_qty_available_resets_shortage_state(self):
        self.assertEqual(self.product.product_state_id, self.shortage_product_state)
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.loc_shelf_1, 15.0
        )
        self.env["product.template"].cron_reset_shortage_states()
        self.assertEqual(self.product.product_state_id, self.default_product_state)

    def test_no_reset_if_not_shortage_state(self):
        self.product.product_state_id = self.test_product_state
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.loc_shelf_1, 15.0
        )
        self.env["product.template"].cron_reset_shortage_states()
        self.assertEqual(self.product.product_state_id, self.test_product_state)

    def test_cannot_be_shortage_and_default(self):
        with self.assertRaises(ValidationError):
            self.default_product_state.is_shortage = True
