# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ABCClassificationProfileLevel(models.Model):
    _name = "abc.classification.profile.level"
    _description = "ABC Classification Profile Level"
    _order = "percentage desc, id desc"

    percentage = fields.Float(default=0.0, required=True, string="%")
    profile_id = fields.Many2one("abc.classification.profile")

    def name_get(self):
        def _get_sort_key_percentage(rec):
            return rec.percentage

        res = []
        for profile in self.mapped("profile_id"):
            for i, level in enumerate(
                profile.level_ids.sorted(key=_get_sort_key_percentage, reverse=True)
            ):
                name = "{} ({}%)".format(chr(65 + i), level.percentage)
                res += [(level.id, name)]
        return res

    @api.constrains("percentage")
    def _check_percentage(self):
        for level in self:
            if level.percentage > 100.0:
                raise ValidationError(_("The percentage cannot be greater than 100."))
            elif level.percentage <= 0.0:
                raise ValidationError(_("The percentage should be a positive number."))
