# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    create_custom_variant = fields.Boolean(
        string="Create custom variant",
        help="When this custom attribute is used, \
        a new value and variant will be generated.",
    )

    @api.constrains(
        "create_custom_variant",
        "is_custom",
    )
    def _constrain_create_custom_variant(self):
        for value in self:
            if value.create_custom_variant and not value.is_custom:
                raise ValidationError(
                    _("'Create custom variant' can only be set on custom values")
                )
