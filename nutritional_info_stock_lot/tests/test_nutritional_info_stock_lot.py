# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon


class TestNutritionalInfoStockLot(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.type_energy = cls.env["nutritional.type"].create(
            {"name": "Energy", "sequence": 10}
        )
        cls.type_fat = cls.env["nutritional.type"].create(
            {"name": "Fat", "sequence": 20}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Lot tracked product",
                "type": "consu",
                "is_storable": True,
                "tracking": "lot",
                "nutritional_value_ids": [
                    Command.create({"type_id": cls.type_energy.id, "value": "200kcal"}),
                    Command.create({"type_id": cls.type_fat.id, "value": "6g"}),
                ],
            }
        )
        cls.product_no_info = cls.env["product.product"].create(
            {
                "name": "Lot tracked product without info",
                "type": "consu",
                "is_storable": True,
                "tracking": "lot",
            }
        )

    def _create_lot(self, product):
        return self.env["stock.lot"].create(
            {"name": f"LOT-{product.id}", "product_id": product.id}
        )

    def test_lot_values_computed_from_product(self):
        """The lot copies the nutritional values defined on its product."""
        lot = self._create_lot(self.product)
        self.assertEqual(len(lot.nutritional_value_ids), 2)
        self.assertEqual(
            lot.nutritional_value_ids.mapped("type_id"),
            self.type_energy + self.type_fat,
        )
        energy_line = lot.nutritional_value_ids.filtered(
            lambda line: line.type_id == self.type_energy
        )
        self.assertEqual(energy_line.value, "200kcal")
        # The related sequence is copied from the type as well.
        self.assertEqual(energy_line.sequence, self.type_energy.sequence)

    def test_lot_without_product_info(self):
        """A lot of a product without nutritional info has no values."""
        lot = self._create_lot(self.product_no_info)
        self.assertFalse(lot.nutritional_value_ids)

    def test_lot_values_are_editable(self):
        """Values are a stored editable compute, so they can be overridden."""
        lot = self._create_lot(self.product)
        energy_line = lot.nutritional_value_ids.filtered(
            lambda line: line.type_id == self.type_energy
        )
        energy_line.value = "999kcal"
        self.assertEqual(energy_line.value, "999kcal")
        # Editing the lot does not propagate back to the product.
        product_energy = self.product.nutritional_value_ids.filtered(
            lambda line: line.type_id == self.type_energy
        )
        self.assertEqual(product_energy.value, "200kcal")

    def test_recompute_on_product_change(self):
        """Changing the product recomputes the nutritional values."""
        lot = self._create_lot(self.product)
        self.assertEqual(len(lot.nutritional_value_ids), 2)
        lot.product_id = self.product_no_info
        self.assertFalse(lot.nutritional_value_ids)

    def test_constraint_repeated_type(self):
        """Repeating a nutritional type on a lot is not allowed."""
        lot = self._create_lot(self.product_no_info)
        with self.assertRaises(UserError):
            lot.write(
                {
                    "nutritional_value_ids": [
                        Command.create(
                            {"type_id": self.type_energy.id, "value": "100kcal"}
                        ),
                        Command.create(
                            {"type_id": self.type_energy.id, "value": "200kcal"}
                        ),
                    ]
                }
            )
