# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    code = fields.Char(
        default="/",
    )

    _sql_constraints = [
        ("uniq_code", "unique(code)", "The category code must be unique!"),
    ]
