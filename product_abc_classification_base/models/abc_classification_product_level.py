# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AbcProductClassificationLevel(models.Model):

    _name = "abc.product.classification.level"
    _description = "Abc Product Classification Level"

    name = fields.Char()

    manual_level_id = fields.Many2one(
        "abc.classification.level", string="Manual classification level"
    )
    computed_level_id = fields.Many2one(
        "abc.classification.level", string="Computed classification level"
    )
    level_id = fields.Many2one(
        "abc.classification.level",
        string="Classification level",
        compute="_compute_level_id",
    )
    flag = fields.Boolean(
        default=False,
        compute="_compute_flag",
        string="If True, this means that the manual classification is different from the computed one",
    )
    product_id = fields.Many2one("product.product", string="Product", index=True)
    # percentage
    profile_id = fields.Many2one("abc.classification.profile", string="Profile")

    @api.depends("manual_level_id", "computed_level_id")
    def _compute_level_id(self):
        for rec in self:
            if rec.manual_level_id:
                rec.level_id = rec.manual_level_id
            else:
                rec.level_id = rec.computed_level_id

    @api.depends("manual_level_id", "computed_level_id")
    def _compute_flag(self):
        for rec in self:
            if rec.manual_level_id != rec.computed_level_id:
                rec.flag = True
