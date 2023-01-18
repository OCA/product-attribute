from odoo import fields, models


class InVitroDiagnostics(models.Model):
    _name = "in.vitro.diagnostic"
    _description = "In vitro diagnostics"

    name = fields.Char(required=True, translate=True)

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "Diagnostic type already exists",
        )
    ]
