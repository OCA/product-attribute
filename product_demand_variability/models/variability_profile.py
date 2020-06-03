# Copyright 2020 ForgeFlow S.L.(http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VariabilityProfile(models.Model):
    _name = "variability.profile"
    _description = "Variability Profile"

    name = fields.Char()
    profile_source = fields.Selection(
        [("actual", "Use actual Stock Moves")],
        help="Information source used for past calculation.",
    )
    profile_horizon_past = fields.Integer(
        string="Past Horizon", help="Length-of-period horizon in days looking past.",
    )
    demand_class_ids = fields.Many2many(
        "variability.profile.class", string="Demand Classes"
    )


class VariabilityProfileClass(models.Model):
    _name = "variability.profile.class"
    _description = "Variability Profile Class"

    name = fields.Char()
    upper_range = fields.Float(help="upper limit of the range within that" " class")
    lower_range = fields.Float(
        help="lower limit of the range within that " "class", default=0.0
    )
