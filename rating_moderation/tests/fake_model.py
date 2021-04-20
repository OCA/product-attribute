# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class FakeModel(models.Model):
    _name = "fake.model"
    _inherit = ["rating.mixin"]
    _description = "testing model"

    name = fields.Char()
