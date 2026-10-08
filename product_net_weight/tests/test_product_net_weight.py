# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestProductNetWeight(BaseCommon):
    _test_user_groups = ("product.group_product_manager", "stock.group_stock_user")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {
                "name": "test attribute",
                "display_type": "select",
            }
        )
        cls.size_values = cls.env["product.attribute.value"].create(
            [
                {"attribute_id": cls.attribute.id, "name": "small"},
                {"attribute_id": cls.attribute.id, "name": "large"},
            ]
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
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.create(
                                    {
                                        "attribute_id": self.attribute.id,
                                        "name": "test value 1",
                                    }
                                ),
                                Command.create(
                                    {
                                        "attribute_id": self.attribute.id,
                                        "name": "test value 2",
                                    }
                                ),
                            ],
                        }
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
        with self.assertRaises(ValidationError):
            self.env["product.product"].create(
                {"name": "Test net weight", "net_weight": 25.0, "weight": 22.0}
            )

    def _create_multi_variant_template(self):
        return self.env["product.template"].create(
            {
                "name": "Test multi variant net weight",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [Command.set(self.size_values.ids)],
                        }
                    )
                ],
            }
        )

    def test_multi_variant_template_net_weight_propagates(self):
        template = self._create_multi_variant_template()
        self.assertEqual(len(template.product_variant_ids), 2)
        with Form(template) as template_form:
            template_form.net_weight = 1.5
        self.assertEqual(template.product_variant_ids.mapped("net_weight"), [1.5, 1.5])

    def test_multi_variant_common_net_weight(self):
        template = self._create_multi_variant_template()
        small, large = template.product_variant_ids
        small.net_weight = 1.2
        large.net_weight = 1.8
        self.assertNotIn(template.net_weight, (1.2, 1.8))
        small.net_weight = 1.8
        self.assertEqual(template.net_weight, 1.8)

    def test_multi_variant_constraint(self):
        template = self._create_multi_variant_template()
        small, large = template.product_variant_ids
        small.weight = 2.0
        large.weight = 5.0
        with self.assertRaises(ValidationError):
            template.net_weight = 3.0
        template.net_weight = 1.5
        self.assertEqual(small.net_weight, 1.5)
        self.assertEqual(large.net_weight, 1.5)
