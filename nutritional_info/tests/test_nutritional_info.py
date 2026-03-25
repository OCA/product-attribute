# Copyright 2026 Takahiro SUNAGA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestNutritionalInfo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.type_energy = cls.env["nutritional.type"].create(
            {"name": "Energy", "sequence": 10}
        )
        cls.type_fat = cls.env["nutritional.type"].create(
            {"name": "Fat", "sequence": 20}
        )
        cls.uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")

    def test_single_variant_compute_inverse(self):
        template = self.env["product.template"].create({"name": "Nutrition test"})
        variant = template.product_variant_id

        self.assertEqual(template.nutritional_reference_qty, 100)
        self.assertEqual(template.nutritional_reference_uom, self.uom_gram)

        template.write(
            {
                "nutritional_reference_qty": 250,
                "nutritional_reference_uom": self.uom_kg.id,
                "nutritional_value_ids": [
                    (0, 0, {"type_id": self.type_energy.id, "value": "200kcal"}),
                    (0, 0, {"type_id": self.type_fat.id, "value": "6g"}),
                ],
            }
        )
        self.assertEqual(variant.nutritional_reference_qty, 250)
        self.assertEqual(variant.nutritional_reference_uom, self.uom_kg)
        self.assertEqual(len(variant.nutritional_value_ids), 2)

        variant.write(
            {
                "nutritional_reference_qty": 80,
                "nutritional_reference_uom": self.uom_gram.id,
            }
        )
        self.assertEqual(template.nutritional_reference_qty, 80)
        self.assertEqual(template.nutritional_reference_uom, self.uom_gram)

    def test_multi_variant_template_fields_do_not_inverse(self):
        attribute = self.env["product.attribute"].create(
            {"name": "Size", "display_type": "radio"}
        )
        value_s = self.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": attribute.id}
        )
        value_m = self.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": attribute.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Multi variant nutrition test",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, [value_s.id, value_m.id])],
                        },
                    )
                ],
            }
        )
        self.assertEqual(template.product_variant_count, 2)

        first_variant = template.product_variant_ids[0]
        second_variant = template.product_variant_ids[1]

        first_variant.write(
            {
                "nutritional_reference_qty": 123,
                "nutritional_reference_uom": self.uom_kg.id,
                "nutritional_value_ids": [
                    (0, 0, {"type_id": self.type_energy.id, "value": "120kcal"})
                ],
            }
        )
        second_variant.write(
            {
                "nutritional_reference_qty": 456,
                "nutritional_reference_uom": self.uom_gram.id,
                "nutritional_value_ids": [
                    (0, 0, {"type_id": self.type_fat.id, "value": "12g"})
                ],
            }
        )

        template.write({"nutritional_reference_qty": 321})
        self.assertEqual(first_variant.nutritional_reference_qty, 123)
        self.assertEqual(second_variant.nutritional_reference_qty, 456)

        template._compute_nutritional_value_ids()
        template._inverse_nutritional_value_ids()
        template._compute_nutritional_reference_uom()
        template._inverse_nutritional_reference_uom()
        template._compute_nutritional_reference_qty()
        template._inverse_nutritional_reference_qty()

        self.assertEqual(first_variant.nutritional_reference_qty, 123)
        self.assertEqual(first_variant.nutritional_reference_uom, self.uom_kg)
        self.assertEqual(len(first_variant.nutritional_value_ids), 1)
        self.assertEqual(second_variant.nutritional_reference_qty, 456)
        self.assertEqual(second_variant.nutritional_reference_uom, self.uom_gram)
        self.assertEqual(len(second_variant.nutritional_value_ids), 1)

    def test_constraint_repeated_nutritional_type(self):
        template = self.env["product.template"].create(
            {"name": "Repeated nutritional type test"}
        )

        with self.assertRaises(UserError):
            template.write(
                {
                    "nutritional_value_ids": [
                        (0, 0, {"type_id": self.type_energy.id, "value": "100kcal"}),
                        (0, 0, {"type_id": self.type_energy.id, "value": "200kcal"}),
                    ]
                }
            )
