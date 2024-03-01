# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    secondary_uom_ids = fields.One2many(
        comodel_name="product.secondary.unit",
        inverse_name="product_id",
        string="Secondary Unit of Measure",
        help="Default Secondary Unit of Measure.",
        context={"active_test": False},
        compute="_compute_secondary_uom_ids",
        inverse="_inverse_secondary_uom_ids",
    )

    @api.depends("product_tmpl_id")
    def _compute_secondary_uom_ids(self):
        for variant in self:
            variant.secondary_uom_ids = (
                variant.product_tmpl_id.secondary_uom_ids.filtered(
                    lambda s, v=variant: s.product_id == v or not s.product_id
                )
            )

    def _inverse_secondary_uom_ids(self):
        for variant in self:
            variant.product_tmpl_id.secondary_uom_ids = (
                variant.product_tmpl_id.secondary_uom_ids.filtered(
                    lambda s, v=variant: s.product_id != v
                )
                + variant.secondary_uom_ids
            )
