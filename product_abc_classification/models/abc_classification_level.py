# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ABCClassificationProfileLevel(models.Model):
    _name = "abc.classification.profile.level"
    _description = "ABC Classification Profile Level"
    _order = "sequence desc, id desc"

    classification_type = fields.Selection(
        related="profile_id.classification_type", string="Classification Type"
    )
    percentage = fields.Float(default=0.0, string="%")
    fixed = fields.Monetary(default=0.0, string="Fixed Value")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        related="profile_id.company_id",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", store=True, related="company_id.currency_id"
    )
    profile_id = fields.Many2one("abc.classification.profile")
    sequence = fields.Integer(
        string="Sequence", compute="_compute_sequence", store=True
    )
    symbol = fields.Char(compute="_compute_symbol", store=True)

    def name_get(self):
        res = []
        for profile in self.mapped("profile_id"):
            classification_type = profile.classification_type
            for i, level in enumerate(
                profile.level_ids.sorted(
                    key=getattr(
                        profile, "_get_sort_key_%s" % profile.classification_type
                    ),
                    reverse=True,
                )
            ):
                name = "{} ({} {})".format(
                    chr(65 + i), level[classification_type], level.symbol
                )
                res += [(level.id, name)]
        return res

    @api.constrains("percentage")
    def _check_percentage(self):
        for level in self:
            if level.classification_type != "percentage":
                continue
            if level.percentage > 100.0:
                raise ValidationError(_("The percentage cannot be greater than 100."))
            elif level.percentage <= 0.0:
                raise ValidationError(_("The percentage should be a positive number."))

    @api.depends("percentage", "fixed", "classification_type")
    def _compute_sequence(self):
        for level in self:
            if level.classification_type == "percentage":
                level.sequence = level.percentage
            elif level.classification_type == "fixed":
                level.sequence = level.fixed

    @api.depends("classification_type")
    def _compute_symbol(self):
        for level in self:
            if level.classification_type == "percentage":
                level.symbol = "%"
            elif level.classification_type == "fixed":
                level.symbol = level.currency_id.symbol
