from odoo import fields, models


class InVitroDiagnostics(models.Model):
    _name = "in.vitro.diagnostic"
    _description = "In vitro diagnostics"

    name = fields.Char(required=True, translate=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "Diagnostic type already exists",
    )
