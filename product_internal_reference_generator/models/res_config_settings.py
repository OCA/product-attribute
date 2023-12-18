# Copyright 2023 Ooops - Ilyas
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    default_int_ref_template_id = fields.Many2one(
        related="company_id.default_int_ref_template_id",
        readonly=False,
    )
