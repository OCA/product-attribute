# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    is_mto = fields.Boolean(
        compute="_compute_is_mto",
        store=True,
    )

    @api.depends("route_ids.is_mto", "categ_id.route_ids.is_mto")
    def _compute_is_mto(self):
        for template in self:
            template.is_mto = bool(
                (template.route_ids | template.route_from_categ_ids).filtered("is_mto")
            )
