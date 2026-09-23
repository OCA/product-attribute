# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    packaging_tmpl_ids = fields.One2many(
        "product.packaging.template", "product_tmpl_id"
    )
