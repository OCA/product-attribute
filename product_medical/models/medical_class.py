# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalClass(models.Model):
    _name = "medical.class"
    _description = "Medical Class"

    name = fields.Char(string="Name", required=True, translate=True)

    _sql_constraints = [("name_uniq", "unique(name)", "Medical class already exists",)]


class InVitroDiagnostics(models.Model):
    _name = "in.vitro.diagnostic"
    _description = "In vitro diagnostics"

    name = fields.Char(string="Name", required=True, translate=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Diagnostic type already exists",)
    ]


class MedicineCategory(models.Model):
    _name = "medicine.category"
    _description = "Medicine Category"

    name = fields.Char(string="Name", required=True, translate=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Medicine category already exists",)
    ]


class PPECategory(models.Model):
    _name = "ppe.category"
    _description = "PPE category"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [("name_uniq", "unique(name)", "PPE category already exists",)]
