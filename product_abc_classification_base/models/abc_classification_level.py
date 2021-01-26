# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AbcClassificationLevel(models.Model):

    _name = "abc.classification.level"
    _order = "percentage desc, id desc"

    percentage = fields.Float(default=0.0, required=True, string="%")
    profile_id = fields.Many2one("abc.classification.profile")

    name = fields.Char(help="Classification A, B or C")  # unique par profile

    @api.constrains("percentage")
    def _check_percentage(self):
        for level in self:
            if level.percentage > 100.0:
                raise ValidationError(_("The percentage cannot be greater than 100."))
            if level.percentage <= 0.0:
                raise ValidationError(_("The percentage should be a positive number."))

