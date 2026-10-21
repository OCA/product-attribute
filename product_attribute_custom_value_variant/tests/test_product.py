# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests import Form

from .common import AttributeValueVariantCommon


class TestSale(AttributeValueVariantCommon):
    def test_creation(self):
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

        # This will simulate the sale behavior that creates custom value at
        # sale order line creation
        custom_value = self.env["product.attribute.custom.value"].create(
            {
                "custom_product_template_attribute_value_id": template_value.id,
                "custom_value": "TEST VALUE",
            }
        )

        with custom_product_variant._get_attribute_custom_value_variant(
            custom_value
        ) as new_variant:
            variant = new_variant

        self.assertNotIn(variant, product_variants)

    def test_custom_value_error(self):
        length_attribute_form = Form(self.env["product.attribute"])
        length_attribute_form.name = "Test custom option attribute"
        with length_attribute_form.value_ids.new() as value:
            value.name = "Custom"
            value.is_custom = False
            value.create_custom_variant = True
        with self.assertRaises(ValidationError):
            self.length_attribute = length_attribute_form.save()
