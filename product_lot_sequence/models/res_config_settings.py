# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """ Inherit res.config.settings to add lot_sequence_padding field. """
    _inherit = "res.config.settings"

    lot_sequence_padding = fields.Integer(
        related="company_id.lot_sequence_padding",
        readonly=False,
    )
