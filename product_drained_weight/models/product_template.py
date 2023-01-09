# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    drained_weight = fields.Float(
        compute="_compute_drained_weight",
        inverse="_inverse_drained_weight",
        digits="Stock Weight",
        help="Drained Weight of the product, fluid excluded.",
        store=True,
    )

    @api.depends("product_variant_ids", "product_variant_ids.drained_weight")
    def _compute_drained_weight(self):
        unique_variants = self.filtered(lambda tmpl: tmpl.product_variant_count == 1)
        for template in unique_variants:
            template.drained_weight = template.product_variant_ids.drained_weight
        for template in self - unique_variants:
            template.drained_weight = 0.0

    def _inverse_drained_weight(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.drained_weight = template.drained_weight

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get("drained_weight"):
                related_vals["drained_weight"] = vals["drained_weight"]
            if related_vals:
                template.write(related_vals)
        return templates
