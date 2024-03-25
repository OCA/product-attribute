# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductionLotIngredientValue(models.Model):
    _name = "production.lot.ingredient.value"
    _description = "Ingredient values for a product lots."
    _rec_name = "ingredient_id"
    _order = "sequence, id"

    sequence = fields.Integer()
    lot_id = fields.Many2one(comodel_name="stock.production.lot")
    # product_id = fields.Many2one(related='lot_id.product_id')
    ingredient_id = fields.Many2one(comodel_name="product.ingredient")
    scientific_name = fields.Char(related="ingredient_id.scientific_name")
    allergen_id = fields.Many2one(related="ingredient_id.allergen_id")
    percentage = fields.Float(digits="Product Unit of Measure")
    is_allergen = fields.Boolean(related="ingredient_id.is_allergen")
