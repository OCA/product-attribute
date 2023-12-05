# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    lot_sequence_id = fields.Many2one(
        "ir.sequence",
        related="company_id.lot_sequence_id",
        readonly=False,
        string="Default lot sequence",
    )
