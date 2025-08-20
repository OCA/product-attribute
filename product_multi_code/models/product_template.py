# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_code_ids = fields.One2many(
        "product.default_code",
        "product_tmpl_id",
        string="Internal References",
    )
