# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    code = fields.Char(
        default="/",
        index=True,
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = default or {}
        default.setdefault("code", self.code + _("-copy"))
        return super().copy(default)
