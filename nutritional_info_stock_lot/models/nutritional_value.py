# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class NutritionalValue(models.Model):
    _inherit = "nutritional.value"
    _name = "nutritional.value.lot"
    _description = "Nutritional values for a given lot"

    lot_id = fields.Many2one(comodel_name="stock.production.lot")
