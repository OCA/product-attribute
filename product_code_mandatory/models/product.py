# Copyright (C) 2018 - TODAY, Open Source Integrators License AGPL-3.0
# or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_default_code(self):
        return self.env["ir.sequence"].next_by_code("product.default.code")

    default_code = fields.Char(
        "Internal Reference", index=True, default=_get_default_code
    )
