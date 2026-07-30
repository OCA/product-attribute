from odoo import fields, models


class PPECategory(models.Model):
    _name = "ppe.category"
    _description = "PPE category"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "PPE category already exists",
    )
