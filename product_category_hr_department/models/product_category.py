# Copyright 2023 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    hr_department_id = fields.Many2one(
        "hr.department", string="Department", required=False
    )
