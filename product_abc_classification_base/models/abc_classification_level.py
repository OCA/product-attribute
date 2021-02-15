# -*- coding: utf-8 -*-
# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AbcClassificationLevel(models.Model):

    _name = "abc.classification.level"
    _order = "percentage desc, id desc"
    _rec_name = "name"

    percentage_products = fields.Float(
        default=0.0, required=True, string="% Products"
    )
    percentage = fields.Float(default=0.0, required=True, string="% Indicator")
    profile_id = fields.Many2one(
        "abc.classification.profile", ondelete="cascade"
    )

    name = fields.Char(help="Classification A, B or C", required=True)

    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE(profile_id, name)",
            _("Level name must be unique by profile"),
        )
    ]

    @api.constrains("percentage")
    def _check_percentage(self):
        for level in self:
            if level.percentage > 100.0:
                raise ValidationError(
                    _("The percentage cannot be greater than 100.")
                )
            if level.percentage <= 0.0:
                raise ValidationError(
                    _("The percentage should be a positive number.")
                )

    @api.constrains("percentage_products")
    def _check_percentage_products(self):
        for level in self:
            if level.percentage_products > 100.0:
                raise ValidationError(
                    _("The percentage of products cannot be greater than 100.")
                )
            if level.percentage_products <= 0.0:
                raise ValidationError(
                    _(
                        "The percentage of products should be a positive number."
                    )
                )
