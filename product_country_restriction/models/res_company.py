# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    default_country_restriction_id = fields.Many2one(
        comodel_name='product.country.restriction',
    )
    country_restriction_strategy = fields.Selection(
        selection=lambda self: self._get_country_restriction_strategy(),
        default=lambda self: self._default_country_restriction_strategy(),

        help='Choose here how your country rules apply.'
             '[Authorize]: Authorize all products but those for which strategy'
             'apply.'
             '[Restrict]: Restrict all products but those for which strategy '
             'apply.'
    )

    @api.model
    def _get_country_restriction_strategy(self):
        return [
            ('authorize', 'Authorize'),
            ('restrict', 'Restrict'),
        ]

    @api.model
    def _default_country_restriction_strategy(self):
        return 'authorize'
