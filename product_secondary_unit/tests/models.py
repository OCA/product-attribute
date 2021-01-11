# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SecondaryUnitFake(models.Model):
    _name = "secondary.unit.fake"
    _inherit = "product.secondary.unit.mixin"
    _description = "Secondary unit fake model for tests"
    _secondary_unit_fields = {
        "qty_field": "product_uom_qty",
        "uom_field": "product_uom_id",
    }

    name = fields.Char()
    product_id = fields.Many2one("product.product", "Product", readonly=True)
    product_uom_qty = fields.Float(
        store=True, readonly=False, compute="_compute_product_uom_qty"
    )
    product_uom_id = fields.Many2one("uom.uom", string="Product Unit of Measure")

    @api.depends("secondary_uom_qty", "secondary_uom_id")
    def _compute_product_uom_qty(self):
        self._compute_helper_target_field_qty()

    @api.onchange("product_uom_id")
    def _onchange_product_uom(self):
        self._onchange_helper_product_uom_for_secondary()
