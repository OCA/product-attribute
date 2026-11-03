# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        (
            "default_code_uniq",
            "unique(default_code)",
            "Internal Reference must be unique across the database!",
        )
    ]

    @api.onchange("default_code")
    def _onchange_default_code(self):
        res = super()._onchange_default_code()
        if isinstance(res, dict):
            res.pop("warning", None)
        return res
