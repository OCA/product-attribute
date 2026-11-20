# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class NutritionalType(models.Model):
    _name = "nutritional.type"
    _description = "Types used to inform about nutritional values at products."
    _order = "sequence, id"

    sequence = fields.Integer(required=True)
    name = fields.Char(translate=True)
