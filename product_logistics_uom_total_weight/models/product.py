# Copyright 2024 Antoni Marroig(APSL-Nagarro)<amarroig@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    total_weight = fields.Float(compute="_compute_total_weight")

    @api.depends("qty_available", "product_weight")
    def _compute_total_weight(self):
        for product in self:
            product.total_weight = (
                product.qty_available * product.product_weight
            ) / product.weight_uom_id.factor


class Product(models.Model):
    _inherit = "product.product"

    total_weight = fields.Float(
        compute="_compute_total_weight",
    )

    @api.depends("qty_available", "product_weight")
    def _compute_total_weight(self):
        for product in self:
            product.total_weight = (
                product.qty_available * product.product_weight
            ) / product.weight_uom_id.factor
