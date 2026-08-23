# Copyright 2020 Tecnativa - Ernesto Tejeda
# Copyright 2023 PESOL - Angel Moya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class UomCategory(models.Model):
    _inherit = "uom.category"

    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide the "
        "product category without removing it.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        categs = super().create(vals_list)
        categs.filtered(lambda x: not x.active).mapped("uom_ids").write(
            {"active": False}
        )
        return categs

    def write(self, vals):
        if "active" in vals and not vals.get("active"):
            self.mapped("uom_ids").write({"active": False})
        return super().write(vals)
