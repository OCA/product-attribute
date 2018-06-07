# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    manufacturer = fields.Boolean(
        string='Is a manufacturer',
        default=False,
        help="Check this box if this contact is a manufacturer."
    )
