# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allergen_id = fields.Many2many(related="product_variant_ids.allergen_id")
    ingredient_ids = fields.One2many(
        related="product_variant_ids.ingredient_ids", readonly=False
    )
    ingredient_allergen_trace_ids = fields.Many2many(
        related="product_variant_ids.ingredient_allergen_trace_ids", readonly=False
    )
    ingredient_additional_info = fields.Text(
        related="product_variant_ids.ingredient_additional_info", readonly=False
    )
