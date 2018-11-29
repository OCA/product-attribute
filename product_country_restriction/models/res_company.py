# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    default_country_restriction_id = fields.Many2one(
        comodel_name='product.country.restriction',
    )
