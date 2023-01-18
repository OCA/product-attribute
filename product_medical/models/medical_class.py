# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalClass(models.Model):
    _name = "medical.class"
    _description = "Medical Class"

    name = fields.Char(required=True, translate=True)

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "Medical class already exists",
        )
    ]
