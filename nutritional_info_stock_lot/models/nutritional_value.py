# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class NutritionalValue(models.Model):
    _inherit = "nutritional.value"

    lot_id = fields.Many2one(comodel_name="stock.production.lot")
