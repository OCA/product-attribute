# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductIngredients(models.Model):
    _name = "product.ingredient"
    _description = "Ingredients of a product."

    name = fields.Char(translate=True)
    scientific_name = fields.Char()
    allergen_id = fields.Many2one(
        comodel_name="product.attribute.value",
        domain=lambda self: [
            ("attribute_id", "=", self.env["product.attribute"].get_allergen_id())
        ],
        context={"set_allergen_attribute": True, "show_attribute": False},
    )
    is_allergen = fields.Boolean()
