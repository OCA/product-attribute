# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    _sql_constraints = [
        ("uniq_code", "unique(code)", "The category code must be unique!"),
    ]

    @api.model
    def _get_next_code(self):
        return self.env["ir.sequence"].next_by_code("product.category")

    @api.model
    def create(self, vals):
        if "code" not in vals or vals["code"] == "/":
            vals["code"] = self._get_next_code()
        return super().create(vals)

    def write(self, vals):
        for category in self:
            value = vals.copy()
            code = value.setdefault("code", category.code)
            if code in [False, "/"]:
                value["code"] = self._get_next_code()
            super().write(value)
        return True
