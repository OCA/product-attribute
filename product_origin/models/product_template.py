# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Origin',
        ondelete='restrict',
        index=True,
    )

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Country State of Origin',
        ondelete='restrict',
        index=True,
    )
