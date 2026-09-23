# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv.expression import NEGATIVE_TERM_OPERATORS

SEPARATOR = ": "


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    @api.model
    def _search_display_name(self, operator, value):
        if value and SEPARATOR in str(value):
            attr_name, val_name = str(value).split(SEPARATOR, 1)
            if operator in NEGATIVE_TERM_OPERATORS:
                return [
                    "|",
                    ("attribute_id.name", operator, attr_name),
                    ("name", operator, val_name),
                ]
            return [
                ("attribute_id.name", operator, attr_name),
                ("name", operator, val_name),
            ]
        return super()._search_display_name(operator, value)
