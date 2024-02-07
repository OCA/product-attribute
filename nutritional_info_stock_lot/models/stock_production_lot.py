# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    nutritional_value_ids = fields.One2many(
        comodel_name="nutritional.value.lot",
        inverse_name="lot_id",
    )

    @api.constrains("nutritional_value_ids", "nutritional_value_ids.type_id")
    def _check_nutritional_type_not_repeated(self):
        for lot in self:
            if lot.nutritional_value_ids and len(lot.nutritional_value_ids) != len(
                lot.nutritional_value_ids.type_id
            ):
                raise UserError(
                    _("Repeating types of nutritional values is not allowed.")
                )
