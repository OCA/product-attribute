# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.fields import Command
from odoo.tests import TransactionCase, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestProductSecondaryUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.template"].create(
            {
                "name": "test",
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    Command.create(
                        {
                            "code": "A",
                            "name": "unit-700",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.7,
                        },
                    ),
                    Command.create(
                        {
                            "code": "B",
                            "name": "unit-900",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.9,
                        },
                    ),
                ],
            }
        )
        cls.woods = cls.env["product.template"].create(
            {
                "name": "Piece of woods",
                "list_price": 2000,
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    Command.create(
                        {
                            "code": "A",
                            "name": "unit-700",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.7,
                        },
                    ),
                    Command.create(
                        {
                            "code": "B",
                            "name": "unit-900",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.9,
                        },
                    ),
                ],
            }
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].search(
            [("product_tmpl_id", "=", cls.product.id)], limit=1
        )
        cls.densitiy = cls.env["product.attribute"].create(
            [
                {
                    "name": "Density",
                    "sequence": 1,
                    "value_ids": [
                        Command.create(
                            {
                                "name": "Low",
                                "sequence": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Heavy",
                                "sequence": 2,
                            }
                        ),
                    ],
                }
            ]
        )
        cls.low, cls.heavy = cls.densitiy.value_ids
        cls.density_attribute_lines = cls.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": cls.woods.id,
                "attribute_id": cls.densitiy.id,
                "value_ids": [Command.set([cls.low.id, cls.heavy.id])],
            }
        )

    def test_product_secondary_unit_name(self):
        self.assertEqual(self.secondary_unit.sudo().display_name, "unit-700-0.7")

    def test_product_secondary_unit_search(self):
        args = [
            (
                "product_tmpl_id.product_variant_ids",
                "in",
                self.product.product_variant_ids.ids,
            )
        ]
        results = self.env["product.secondary.unit"].name_search(name="A", args=args)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][1],
            self.env["product.secondary.unit"]
            .browse(results[0][0])
            .sudo()
            .display_name,
        )
        results = self.env["product.secondary.unit"].name_search(name="X", args=args)
        self.assertEqual(len(results), 0)

    def test_multi_variant_product_secondary_unit(self):
        first_variant = self.woods.product_variant_ids[0]
        second_variant = self.woods.product_variant_ids[1]
        self.assertEqual(len(self.woods.secondary_uom_ids), 2)
        self.assertEqual(first_variant.secondary_uom_ids, self.woods.secondary_uom_ids)
        first_variant.write(
            {
                "secondary_uom_ids": [
                    Command.create(
                        {
                            "code": "C",
                            "name": "unit-1000",
                            "product_id": first_variant.id,
                            "uom_id": self.product_uom_unit.id,
                            "factor": 0.1,
                        }
                    )
                ]
            }
        )
        first_variant.invalidate_recordset()
        self.assertEqual(len(self.woods.secondary_uom_ids), 3)
        self.assertEqual(len(first_variant.secondary_uom_ids), 3)
        self.assertEqual(len(second_variant.secondary_uom_ids), 2)
