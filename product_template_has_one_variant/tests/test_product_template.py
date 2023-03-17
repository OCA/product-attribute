# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductTemplateHasOneVariant(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductAttribute = cls.env["product.attribute"]
        cls.ProductAttributeValue = cls.env["product.attribute.value"]
        cls.attribute_color = cls.ProductAttribute.create(
            {"name": "Color", "sequence": 1}
        )

        # Product Attribute color Value
        cls.attribute_color_red = cls.ProductAttributeValue.create(
            {"name": "red", "attribute_id": cls.attribute_color.id, "sequence": 1}
        )
        cls.attribute_color_blue = cls.ProductAttributeValue.create(
            {"name": "blue", "attribute_id": cls.attribute_color.id, "sequence": 2}
        )
        cls.product = cls.env["product.template"].create(
            {
                "name": "One Variant Template",
            }
        )

    def test_template_one_variant(self):
        # By default, templates are created with one variant
        self.assertTrue(self.product.has_one_variant)

        self.product.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attribute_color.id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        self.attribute_color_red.id,
                                        self.attribute_color_blue.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ]
            }
        )
        self.assertFalse(self.product.has_one_variant)
