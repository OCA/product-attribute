# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductPackagingTemplate(models.Model):
    _inherit = "product.packaging.template"

    purchase = fields.Boolean(
        default=True, help="If true, the packaging can be used for purchase orders"
    )

    @api.model
    def _get_values_to_propagate(self, vals):
        res = super()._get_values_to_propagate(vals)
        if "purchase" in vals:
            res["purchase"] = vals["purchase"]
        return res

    def _prepare_create_values_for_packaging(self):
        res = super()._prepare_create_values_for_packaging()
        res["purchase"] = self.purchase
        return res
