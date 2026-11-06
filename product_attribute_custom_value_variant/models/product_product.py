# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections.abc import Generator
from contextlib import contextmanager

from odoo import models

from odoo.addons.product.models.product_product import ProductProduct as ProductBase


class ProductProduct(models.Model):
    _inherit = "product.product"

    @contextmanager
    def _get_attribute_custom_value_variant(
        self, custom_values
    ) -> Generator[ProductBase | None]:
        """
        This will retrieve the new created variant as context manager return.

        At the end, it will:

            - Remove the attributes
            - Remove the
        """

        new_attribute_values, custom_values_to_unlink = (
            custom_values._get_new_and_unlink_custom_attribute()
        )
        # If new attribute values have been created,
        # use them to create a new variant and set it in the line
        attribute_lines = self.product_tmpl_id.attribute_line_ids
        custom_combination = attribute_lines.product_template_value_ids.filtered(
            lambda ptav, new=new_attribute_values: ptav.product_attribute_value_id
            in new
        )
        if custom_combination:
            new_variant = self._create_custom_attribute_combination(custom_combination)
            yield new_variant
            # The new attribute values must not be available for new models
            for attribute_line in attribute_lines:
                attribute_line.with_context(
                    no_remove_custom_variants=new_variant.ids,
                ).value_ids -= attribute_line.value_ids & new_attribute_values
        custom_values_to_unlink.unlink()

    def _create_custom_attribute_combination(self, custom_combination):
        self.ensure_one()
        variant_combination = self.product_template_attribute_value_ids
        new_variant_combination = (
            variant_combination.filtered(
                lambda ptav: not ptav.product_attribute_value_id.create_custom_variant
            )
            | custom_combination
        )
        new_variant = self.product_tmpl_id._create_product_variant(
            new_variant_combination
        )
        return new_variant

    def _unlink_or_archive(self, check_access=True):
        custom_variants_to_keep_ids = self.env.context.get("no_remove_custom_variants")
        return super(
            ProductProduct, self - self.browse(custom_variants_to_keep_ids)
        )._unlink_or_archive(check_access=check_access)
