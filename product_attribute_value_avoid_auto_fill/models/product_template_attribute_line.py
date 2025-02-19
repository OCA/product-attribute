# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductAttribute(models.Model):
    _inherit = "product.template.attribute.line"

    @api.onchange("attribute_id")
    def _onchange_attribute_id(self):
        # Avoid auto fill when option is selected
        if (
            not self.attribute_id.avoid_fill_all_values
            or self.attribute_id.create_variant != "no_variant"
        ):
            return super()._onchange_attribute_id()
        self.value_ids = False
