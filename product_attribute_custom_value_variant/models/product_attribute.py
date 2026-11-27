# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    def _prepare_variant_custom_attribute_value(self, custom_value):
        self.ensure_one()
        return {
            "attribute_id": self.id,
            "name": custom_value,
        }

    def _get_variant_custom_attribute_value(self, custom_value):
        self.ensure_one()
        new_attribute_value = self.env["product.attribute.value"].search(
            [
                (
                    "attribute_id",
                    "=",
                    self.id,
                ),
                ("name", "=", custom_value),
            ],
            limit=1,
        )
        if not new_attribute_value:
            new_attribute_value = self.env["product.attribute.value"].create(
                self._prepare_variant_custom_attribute_value(custom_value)
            )

        return new_attribute_value
