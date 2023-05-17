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

    @api.onchange("active")
    def _onchange_active(self):
        if not self.active:
            self.uom_ids.active = False

    @api.onchange("uom_ids")
    def _onchange_uom_ids(self):
        if self.active:
            return super()._onchange_uom_ids()
