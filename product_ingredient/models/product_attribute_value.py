# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("set_allergen_attribute"):
            res["attribute_id"] = self.env["product.attribute"].get_allergen_id()
        return res
