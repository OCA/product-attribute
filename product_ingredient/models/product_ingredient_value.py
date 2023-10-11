# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductIngredientValue(models.Model):
    _name = "product.ingredient.value"
    _description = "Ingredient values for a product."
    _rec_name = "ingredient_id"
    _order = "sequence, id"

    sequence = fields.Integer()
    product_id = fields.Many2one(comodel_name="product.product")
    ingredient_id = fields.Many2one(comodel_name="product.ingredient")
    scientific_name = fields.Char(related="ingredient_id.scientific_name")
    allergen_id = fields.Many2one(related="ingredient_id.allergen_id")
    percentage = fields.Float(digits="Product Unit of Measure")
    is_allergen = fields.Boolean(related="ingredient_id.is_allergen")
