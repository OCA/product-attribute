from odoo import fields, models


class MedicineCategory(models.Model):
    _name = "medicine.category"
    _description = "Medicine Category"

    name = fields.Char(required=True, translate=True)

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "Medicine category already exists",
        )
    ]
