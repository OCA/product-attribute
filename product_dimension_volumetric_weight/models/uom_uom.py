# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    volumetric_weight_ratio = fields.Float(
        string="Volumetric Weight Ratio (Kg/m3)",
        help="Used as variable for the volumetric weight calculation "
        "using the formula. (Volume * Ratio) = Kg",
        default=100,
        digits="Stock Weight",
    )
