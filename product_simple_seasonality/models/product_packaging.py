# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    seasonality_ids = fields.Many2many(
        "seasonality",
        related="product_id.seasonality_ids",
    )
