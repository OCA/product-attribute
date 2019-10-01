# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_artist = fields.Boolean()
    is_label = fields.Boolean()
    company_type = fields.Selection(
        selection_add=[('artist', 'Artist'), ('label', 'Label')]
    )

    @api.depends('is_company')
    def _compute_company_type(self):
        # No call to super to avoid the default on person before another update
        for partner in self:
            if partner.is_company:
                partner.company_type = 'company'
            elif partner.is_artist:
                partner.company_type = 'artist'
            elif partner.is_label:
                partner.company_type = 'label'
            else:
                partner.company_type = 'person'

    def _write_company_type(self):
        for partner in self:
            partner.is_artist = partner.company_type == 'artist'
            partner.is_label = partner.company_type == 'label'
        return super()._write_company_type()

    @api.onchange('company_type')
    def onchange_company_type(self):
        self.is_artist = (self.company_type == 'artist')
        self.is_label = (self.company_type == 'label')
        return super().onchange_company_type()
