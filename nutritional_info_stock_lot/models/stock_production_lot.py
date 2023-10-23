# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    nutritional_value_ids = fields.One2many(
        comodel_name="nutritional.value.lot",
        inverse_name="lot_id",
    )
