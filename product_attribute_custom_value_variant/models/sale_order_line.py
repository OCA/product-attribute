# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models

from odoo.addons.product.models.product_attribute_custom_value import (
    ProductAttributeCustomValue,
)
from odoo.addons.product.models.product_attribute_value import ProductAttributeValue


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_new_and_unlink_custom_attribute(
        self,
    ) -> tuple[ProductAttributeValue, ProductAttributeCustomValue]:
        """
        Retrieve the new custom attribute from custom value and
        the one to remove
        """
        self.ensure_one()
        # Create new attribute values for each "Create custom variant" custom value
        values_to_unlink = self.env["product.attribute.custom.value"].browse()
        new_attribute_values = self.env["product.attribute.value"].browse()
        # Create new attribute values for each "Create custom variant" custom value
        for custom_attribute_value in self.product_custom_attribute_value_ids:
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

    def _create_custom_attribute_combination(
        self, custom_combination, attribute_lines, new_attribute_values
    ) -> None:
        self.ensure_one()
        variant_combination = self.product_id.product_template_attribute_value_ids
        new_variant_combination = (
            variant_combination.filtered(
                lambda ptav: not ptav.product_attribute_value_id.create_custom_variant
            )
            | custom_combination
        )
        new_variant = self.product_template_id._create_product_variant(
            new_variant_combination
        )
        self.product_id = new_variant
        # The new attribute values must not be available for new models
        for attribute_line in attribute_lines:
            attribute_line.with_context(
                no_remove_custom_variants=new_variant.ids,
            ).value_ids -= attribute_line.value_ids & new_attribute_values

    def _assign_new_custom_variant(self):
        """Create new variants and assign them to the `self`."""
        custom_values_to_unlink = self.env["product.attribute.custom.value"].browse()
        for line in self:
            new_attribute_values, custom_values_to_unlink = (
                self._get_new_and_unlink_custom_attribute()
            )
            custom_values_to_unlink |= custom_values_to_unlink

            # If new attribute values have been created,
            # use them to create a new variant and set it in the line
            attribute_lines = line.product_template_id.attribute_line_ids
            custom_combination = attribute_lines.product_template_value_ids.filtered(
                lambda ptav, new=new_attribute_values: ptav.product_attribute_value_id
                in new
            )
            if custom_combination:
                self._create_custom_attribute_combination(
                    custom_combination, attribute_lines, new_attribute_values
                )

        if custom_values_to_unlink:
            custom_values_to_unlink.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        custom_value_lines = lines.filtered("product_custom_attribute_value_ids")
        if custom_value_lines:
            custom_value_lines._assign_new_custom_variant()
        return lines
