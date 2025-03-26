# Copyright (C) 2025  Renato Lima - Akretion
# License LGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class UomAlias(models.Model):
    _name = "uom.alias"
    _description = "UOM Alias"
    _rec_name = "code"

    code = fields.Char()

    uom_id = fields.Many2one(comodel_name="uom.uom")

    _sql_constraints = [
        (
            "uom_alias_unique",
            "UNIQUE(code)",
            "You cannot repeat the alias name",
        )
    ]
