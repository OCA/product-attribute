# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestSale(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test customer",
            }
        )

        length_attribute_form = Form(cls.env["product.attribute"])
        length_attribute_form.name = "Test length attribute"
        with length_attribute_form.value_ids.new() as value:
            value.name = "5"
        with length_attribute_form.value_ids.new() as value:
            value.name = "10"
        with length_attribute_form.value_ids.new() as value:
            value.name = "Custom"
            value.is_custom = True
            value.create_custom_variant = True
        cls.length_attribute = length_attribute_form.save()

        glass_product_template_form = Form(cls.env["product.template"])
        glass_product_template_form.name = "Glass"
        with glass_product_template_form.attribute_line_ids.new() as length_attribute_line:
            length_attribute_line.attribute_id = cls.length_attribute
            for value in cls.length_attribute.value_ids:
                length_attribute_line.value_ids.add(value)
        cls.glass_product_template = glass_product_template_form.save()

    def test_sale(self):
        """When a product template is sold with a "Create custom variant" attribute value,
        a new attribute value is created and assigned to the new sold variant."""
        customer = self.customer
        product_template = self.glass_product_template
        attribute = self.length_attribute
        attribute_values = attribute.value_ids
        attribute_value = attribute_values.filtered("create_custom_variant")
        template_value = (
            product_template.attribute_line_ids.product_template_value_ids.filtered(
                lambda ptav: ptav.product_attribute_value_id == attribute_value
            )
        )
        product_variants = product_template.product_variant_ids
        custom_product_variant = product_variants.filtered(
            lambda variant: template_value
            in variant.product_template_attribute_value_ids
        )
        # pre-condition
        self.assertTrue(template_value.product_attribute_value_id.create_custom_variant)

        # Act
        custom_values_commands = [
            Command.create(
                {
                    "custom_product_template_attribute_value_id": template_value.id,
                    "custom_value": "15",
                }
            ),
        ]
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": customer.id,
                "order_line": [
                    Command.create(
                        {
                            "name": "Test line",
                            "product_id": custom_product_variant.id,
                            "product_custom_attribute_value_ids": custom_values_commands,
                        }
                    )
                ],
            }
        )

        # Assert
        sold_variant = sale_order.order_line.product_id
        self.assertNotIn(sold_variant, product_variants)
        self.assertIn(sold_variant, product_template.product_variant_ids)

        new_attribute_value = attribute.value_ids - attribute_values
        sold_variant_attribute_values = (
            sold_variant.product_template_attribute_value_ids.product_attribute_value_id
        )
        self.assertIn(new_attribute_value, sold_variant_attribute_values)
        self.assertNotIn(attribute_value, sold_variant_attribute_values)
        self.assertNotIn(new_attribute_value, sold_variant.attribute_line_ids.value_ids)
