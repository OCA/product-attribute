# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests.common import TransactionCase


class TestProductPackagingTemplate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["product.template"].create(
            {
                "name": "Test Product",
            }
        )
        cls.attribute_color = cls.env.ref("product.product_attribute_2")
        cls.attribute_line = cls.env["product.template.attribute.line"].create(
            [
                {
                    "product_tmpl_id": cls.template.id,
                    "attribute_id": cls.attribute_color.id,
                    "value_ids": [
                        Command.set(
                            [
                                cls.env.ref("product.product_attribute_value_3").id,
                                cls.env.ref("product.product_attribute_value_4").id,
                            ]
                        ),
                    ],
                }
            ]
        )
        cls.variant_1 = cls.template.product_variant_ids[0]
        cls.variant_2 = cls.template.product_variant_ids[0]

    def test_create_packaging_template(self):
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 10", "qty": 10})
        ]
        self.assertEqual(len(self.variant_1.packaging_ids), 1)
        self.assertEqual(len(self.variant_2.packaging_ids), 1)
        self.assertEqual(self.variant_1.packaging_ids.name, "Box of 10")
        self.assertEqual(self.variant_2.packaging_ids.name, "Box of 10")

    def test_update_packaging_template(self):
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 10", "qty": 10})
        ]
        self.template.packaging_tmpl_ids.write({"name": "Box of 12", "qty": 12})
        self.assertEqual(self.variant_1.packaging_ids.name, "Box of 12")
        self.assertEqual(self.variant_2.packaging_ids.name, "Box of 12")
        self.assertEqual(self.variant_1.packaging_ids.qty, 12)
        self.assertEqual(self.variant_2.packaging_ids.qty, 12)

    def test_delete_packaging_template(self):
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 10", "qty": 10})
        ]
        self.assertEqual(len(self.template.packaging_tmpl_ids.packaging_ids), 2)
        # Manually delete the packaging on variant 2
        self.variant_2.packaging_ids.unlink()
        self.assertEqual(len(self.template.packaging_tmpl_ids), 1)
        self.assertEqual(len(self.template.packaging_tmpl_ids.packaging_ids), 1)
        # Delete the template
        self.template.packaging_tmpl_ids.unlink()
        self.assertFalse(self.variant_1.packaging_ids)

    def test_create_new_variant(self):
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 10", "qty": 10})
        ]
        self.assertEqual(len(self.template.packaging_tmpl_ids.packaging_ids), 2)
        self.attribute_line.value_ids = [
            Command.link(self.env.ref("product.product_attribute_value_color_wood").id)
        ]
        self.assertEqual(len(self.template.packaging_tmpl_ids.packaging_ids), 3)
