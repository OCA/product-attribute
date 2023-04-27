# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class NutritionalValue(models.Model):
    _name = "nutritional.value"
    _description = "Nutritional values for a given product"
    _order = "sequence, id"

    type_id = fields.Many2one(comodel_name="nutritional.type")
    value = fields.Char()
    sequence = fields.Integer(related="type_id.sequence")
    product_id = fields.Many2one(comodel_name="product.product")
