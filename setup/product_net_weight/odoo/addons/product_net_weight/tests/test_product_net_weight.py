# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestProductNetWeight(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {
                "name": "test attribute",
                "display_type": "select",
            }
        )

    def test_create_product_template(self):
        product_form = Form(self.env["product.template"])
        product_form.name = "Test net weight"
        product_form.net_weight = 25.0
        product = product_form.save()
        self.assertEqual(product.net_weight, 25.0)
        self.assertEqual(product.product_variant_id.net_weight, 25.0)
        product.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "attribute_id": self.attribute.id,
                                        "name": "test value 1",
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "attribute_id": self.attribute.id,
                                        "name": "test value 2",
                                    },
                                ),
                            ],
                        },
                    )
                ]
            }
        )
        self.assertEqual(product.net_weight, 0.0)

    def test_create_product_product(self):
        product_form = Form(self.env["product.product"])
        product_form.name = "Test net weight"
        product_form.net_weight = 25.0
        product = product_form.save()
        self.assertEqual(product.net_weight, 25.0)
        self.assertEqual(product.product_variant_id.net_weight, 25.0)

    def test_product_constraint(self):
        product_form = Form(self.env["product.product"])
        product_form.name = "Test net weight"
        product_form.net_weight = 25.0
        product_form.weight = 22.0
        with self.assertRaises(ValidationError):
            product_form.save()
