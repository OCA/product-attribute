from odoo import fields, models


class PPECategory(models.Model):
    _name = "ppe.category"
    _description = "PPE category"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "PPE category already exists",
        )
    ]
