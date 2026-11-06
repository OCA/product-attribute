# Copyright (C) 2018 - TODAY, Open Source Integrators License AGPL-3.0
# or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _prepare_variant_values(self, combination):
        res = super()._prepare_variant_values(combination)
        # Only a template with a single variant passes its code on. With
        # attributes, each variant gets its own unique code.
        if self.default_code and not self.attribute_line_ids:
            res.update({"default_code": self.default_code})
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_default_code(self):
        return self.env["ir.sequence"].next_by_code("product.default.code")

    default_code = fields.Char(default=lambda self: self._get_default_code())
