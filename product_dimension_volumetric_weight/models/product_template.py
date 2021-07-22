# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    volumetric_weight = fields.Float(
        string="Volumetric weight",
        compute="_compute_volumetric_weight",
        store=True,
        digits="Stock Weight",
    )

    @api.depends("dimensional_uom_id", "volume")
    def _compute_volumetric_weight(self):
        for item in self:
            item.volumetric_weight = (
                item.volume * item.dimensional_uom_id.volumetric_weight_ratio
            )
