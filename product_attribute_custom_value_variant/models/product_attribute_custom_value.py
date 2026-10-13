# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.product.models.product_attribute_custom_value import (
    ProductAttributeCustomValue,
)
from odoo.addons.product.models.product_attribute_value import ProductAttributeValue


class ProductAttribute(models.Model):
    _inherit = "product.attribute.custom.value"

    def _get_new_and_unlink_custom_attribute(
        self,
    ) -> tuple[ProductAttributeValue, ProductAttributeCustomValue]:
        """
        Retrieve the new custom attribute from custom value and
        the one to remove
        """
        values_to_unlink = self.env["product.attribute.custom.value"].browse()
        new_attribute_values = self.env["product.attribute.value"].browse()
        # Create new attribute values for each "Create custom variant" custom value
        for custom_attribute_value in self:
            template_attribute_value = (
                custom_attribute_value.custom_product_template_attribute_value_id
            )
            attribute_value = template_attribute_value.product_attribute_value_id
            if attribute_value.create_custom_variant:
                attribute = template_attribute_value.attribute_id
                new_attribute_value = attribute._get_variant_custom_attribute_value(
                    custom_attribute_value.custom_value,
                )
                new_attribute_values |= new_attribute_value
                template_attribute_value.attribute_line_id.value_ids |= (
                    new_attribute_value
                )

                values_to_unlink |= custom_attribute_value
        return new_attribute_values, values_to_unlink
