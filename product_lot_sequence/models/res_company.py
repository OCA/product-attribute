# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    """ Inherit res.company to add lot_sequence_padding field """
    _inherit = "res.company"

    lot_sequence_padding = fields.Integer("Sequence Number of Digits", default=7)
