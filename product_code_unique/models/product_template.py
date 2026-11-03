# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("default_code")
    def _onchange_default_code(self):
        res = super()._onchange_default_code()
        if isinstance(res, dict):
            res.pop("warning", None)
        return res
