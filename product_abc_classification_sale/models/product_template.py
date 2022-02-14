# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seasonality_classification = fields.Selection(
        selection=[
            ("very high", "Very high"),
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ],
        compute="_compute_seasonality_classification",
        inverse="_inverse_seasonality_classification",
        search="_search_seasonality_classification",
        readonly=False,
    )

    @api.depends(
        "product_variant_ids", "product_variant_ids.seasonality_classification"
    )
    def _compute_seasonality_classification(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.seasonality_classification = (
                template.product_variant_ids.seasonality_classification
            )
        for template in self - unique_variants:
            template.seasonality_classification = False

    def _inverse_seasonality_classification(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.seasonality_classification = (
                self.seasonality_classification
            )

    def _search_seasonality_classification(self, operator, value):
        products = self.env["product.product"].search(
            [("seasonality_classification", operator, value)], limit=None
        )
        return [("id", "in", products.mapped("product_tmpl_id").ids)]
