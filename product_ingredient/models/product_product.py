# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    allergen_id = fields.Many2many(
        comodel_name="product.attribute.value", compute="_compute_allergen_id"
    )
    ingredient_ids = fields.One2many(
        comodel_name="product.ingredient.value", inverse_name="product_id"
    )
    ingredient_allergen_trace_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Allergen traces",
        domain=lambda self: [
            ("attribute_id", "=", self.env["product.attribute"].get_allergen_id())
        ],
        context={"set_allergen_attribute": True, "show_attribute": False},
    )
    ingredient_additional_info = fields.Text(translate=True)

    @api.depends("ingredient_ids", "ingredient_allergen_trace_ids")
    def _compute_allergen_id(self):
        for product in self:
            product.allergen_id = (
                product.ingredient_ids.mapped("allergen_id")
                + product.ingredient_allergen_trace_ids
            )
