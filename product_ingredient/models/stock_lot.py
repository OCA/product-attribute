# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    ingredient_ids = fields.One2many(
        comodel_name="stock.lot.ingredient.value",
        inverse_name="lot_id",
        compute="_compute_ingredient_values",
        store=True,
        readonly=False,
    )
    ingredient_allergen_trace_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        compute="_compute_ingredient_values",
        readonly=False,
        domain=lambda self: [
            ("attribute_id", "=", self.env["product.attribute"].get_allergen_id())
        ],
        context={"set_allergen_attribute": True, "show_attribute": False},
        store=True,
    )
    ingredient_additional_info = fields.Text(
        compute="_compute_ingredient_values", readonly=False, store=True, translate=True
    )

    @api.depends("product_id")
    def _compute_ingredient_values(self):
        for lot in self:
            ingredient_list = [Command.clear()]
            for ingredient_line in lot.product_id.ingredient_ids:
                ingredient_list.append(
                    Command.create(
                        {
                            "sequence": ingredient_line.sequence,
                            "ingredient_id": ingredient_line.ingredient_id.id,
                            "percentage": ingredient_line.percentage,
                        },
                    )
                )
            lot.ingredient_ids = ingredient_list
            lot.ingredient_allergen_trace_ids = (
                lot.product_id.ingredient_allergen_trace_ids
            )
            lot.ingredient_additional_info = lot.product_id.ingredient_additional_info
