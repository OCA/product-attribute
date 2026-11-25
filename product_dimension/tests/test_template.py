# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests.common import TransactionCase


class TestTemplateValues(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Unittest P1",
                "product_length": 10.0,
                "product_width": 5.0,
                "product_height": 3.0,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "type": "consu",
            }
        )
        cls.size_attribute = cls.env["product.attribute"].create({"name": "Size"})
        cls.size_val_s = cls.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": cls.size_attribute.id}
        )
        cls.size_val_m = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.size_attribute.id}
        )

    def test_template(self):
        """
        Data:
            one product template with dimensions
        Test Case:
            get the product associated to the product_template and
            check that the length, width and height
            are the same as for the product template
        Expected result:
            length, width, height are the same on the product and product template
        """

        product = self.product_template.product_variant_ids

        self.assertEqual(product.product_length, 10.0)
        self.assertEqual(product.product_width, 5.0)
        self.assertEqual(product.product_height, 3.0)

    def test_template_create(self):
        """The UoM of the template is propagated to the variant"""
        uom = self.env.ref("uom.product_uom_meter")
        product_template = self.env["product.template"].create(
            {
                "name": "Unittest P2",
                "dimensional_uom_id": uom.id,
                "type": "consu",
            }
        )
        self.assertEqual(product_template.dimensional_uom_id, uom)
        self.assertEqual(product_template.product_variant_ids.dimensional_uom_id, uom)

    def test_template_multi_variant_volume(self):
        """Make sure multi-variant template computes and updates volume correctly."""
        template = self.env["product.template"].create(
            {
                "name": "Multi Variant P3",
                "type": "consu",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.size_attribute.id,
                            "value_ids": [
                                Command.link(self.size_val_s.id),
                                Command.link(self.size_val_m.id),
                            ],
                        }
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 2)
        v1, v2 = template.product_variant_ids

        v1.volume = 2.0
        v2.volume = 2.0
        self.assertEqual(template.volume, 2.0)

        v1.volume = 1.0
        self.assertEqual(template.volume, 2.0)

        uom_m = self.env.ref("uom.product_uom_meter")
        v1.write(
            {
                "product_length": 2.0,
                "product_height": 3.0,
                "product_width": 4.0,
                "dimensional_uom_id": uom_m.id,
            }
        )
        v2.write(
            {
                "product_length": 2.0,
                "product_height": 3.0,
                "product_width": 4.0,
                "dimensional_uom_id": uom_m.id,
            }
        )
        self.assertEqual(v1.volume, 24.0)
        self.assertEqual(v2.volume, 24.0)
        self.assertEqual(template.volume, 24.0)

        template.volume = 5.0
        self.assertEqual(v1.volume, 5.0)
        self.assertEqual(v2.volume, 5.0)
        self.assertEqual(template.volume, 5.0)
