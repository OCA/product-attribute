# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    nutritional_value_ids = fields.One2many(
        comodel_name="nutritional.value.lot",
        inverse_name="lot_id",
        compute="_compute_nutritional_value_ids",
        store=True,
        readonly=False,
    )

    @api.depends("product_id")
    def _compute_nutritional_value_ids(self):
        for lot in self:
            nutritional_list = [(5, 0, 0)]
            for nutritional_line in lot.product_id.nutritional_value_ids:
                nutritional_list.append(
                    (
                        0,
                        0,
                        {
                            "type_id": nutritional_line.type_id.id,
                            "sequence": nutritional_line.sequence,
                            "product_id": nutritional_line.product_id.id,
                            "value": nutritional_line.value,
                        },
                    )
                )
            lot.nutritional_value_ids = nutritional_list

    @api.constrains("nutritional_value_ids", "nutritional_value_ids.type_id")
    def _check_nutritional_type_not_repeated(self):
        for lot in self:
            if lot.nutritional_value_ids and len(lot.nutritional_value_ids) != len(
                lot.nutritional_value_ids.type_id
            ):
                raise UserError(
                    _("Repeating types of nutritional values is not allowed.")
                )
