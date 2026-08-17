# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductPackagingTemplate(models.Model):
    _inherit = "product.packaging.template"

    sales = fields.Boolean(
        default=True, help="If true, the packaging can be used for sales orders"
    )

    @api.model
    def _get_values_to_propagate(self, vals):
        res = super()._get_values_to_propagate(vals)
        if "sales" in vals:
            res["sales"] = vals["sales"]
        return res

    def _prepare_create_values_for_packaging(self):
        res = super()._prepare_create_values_for_packaging()
        res["sales"] = self.sales
        return res
