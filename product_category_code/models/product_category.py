# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    code = fields.Char(
        default="/",
        index=True,
    )

    def copy(self, default=None):
        default = default or {}
        default.setdefault("code", self.code + self.env._("-copy"))
        return super().copy(default)
