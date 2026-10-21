# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class AttributeValueVariantCommon(BaseCommon):
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
        lines = glass_product_template_form.attribute_line_ids
        with lines.new() as length_attribute_line:
            length_attribute_line.attribute_id = cls.length_attribute
            for value in cls.length_attribute.value_ids:
                length_attribute_line.value_ids.add(value)
        cls.glass_product_template = glass_product_template_form.save()
