# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields
from odoo.tests.common import TransactionCase


class TestVariants(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.uom_cm = cls.env["uom.uom"].search([("name", "=", "cm")])
        cls.product_attribute_1 = cls.env.ref("product.product_attribute_1")
        cls.product_attribute_value_1 = cls.env.ref("product.product_attribute_value_1")
        cls.product_attribute_value_2 = cls.env.ref("product.product_attribute_value_2")
        cls.test_product_template_1 = cls.env["product.template"].create(
            {
                "name": "test product template 1",
                "dimensional_uom_id": cls.uom_cm.id,
                "weight": 2.0,
                "product_length": 100.0,
                "product_width": 50.0,
                "product_height": 30.0,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "type": "consu",
            }
        )

    def test_create_variant_keeps_product_dimensions(self):
        """
        Test that creating a new variant keeps all product dimensions.
        """
        variant_1 = self.test_product_template_1.product_variant_ids
        self.assertEqual(variant_1.dimensional_uom_id, self.uom_cm)
        self.assertAlmostEqual(variant_1.volume, 0.15)
        self.test_product_template_1.write(
            {
                "attribute_line_ids": [
                    fields.Command.create(
                        {
                            "attribute_id": self.product_attribute_1.id,
                            "value_ids": [
                                fields.Command.set(
                                    [
                                        self.product_attribute_value_1.id,
                                        self.product_attribute_value_2.id,
                                    ],
                                ),
                            ],
                        },
                    ),
                ]
            }
        )
        for variant in self.test_product_template_1.product_variant_ids:
            self.assertEqual(variant.dimensional_uom_id, self.uom_cm)
            self.assertEqual(variant.product_length, 100.0)
            self.assertEqual(variant.product_width, 50.0)
            self.assertEqual(variant.product_height, 30.0)
            self.assertAlmostEqual(variant.volume, 0.15)
