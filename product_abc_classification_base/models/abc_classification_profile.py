# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AbcClassificationProfile(models.Model):

    _name = "abc.classification.profile"
    _description = "Abc Classification Profile"

    name = fields.Char()
    level_ids = fields.Many2many(
        comodel_name="abc.classification.level", inverse_name="profile_id"
    )
    display_name = fields.Char()

    profile_type = fields.Selection(
        selection=[], string="Type of ABC classification", index=True, required=True
    )
    period = fields.Integer(
        default=365,
        string="Period on which to compute the classification (Days)",
        required=True,
    )

    def _fill_initial_product_data(self, date):
        raise NotImplementedError()

    def _fill_data_(self, date, product_list):
        raise NotImplementedError()

    @api.model
    def _compute_abc_classification(self):
        raise NotImplementedError()
