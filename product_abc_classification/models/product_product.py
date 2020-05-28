# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    abc_classification_profile_id = fields.Many2one(
        "abc.classification.profile",
        compute="_compute_abc_classification_profile_id",
        inverse="_inverse_abc_classification_profile_id",
        store=True,
    )
    abc_classification_level_id = fields.Many2one(
        "abc.classification.profile.level",
        compute="_compute_abc_classification_level_id",
        inverse="_inverse_abc_classification_level_id",
        store=True,
    )

    @api.depends(
        "product_variant_ids", "product_variant_ids.abc_classification_profile_id"
    )
    def _compute_abc_classification_profile_id(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.abc_classification_profile_id = (
                template.product_variant_ids.abc_classification_profile_id
            )
        for template in self - unique_variants:
            template.abc_classification_profile_id = False

    @api.depends(
        "product_variant_ids", "product_variant_ids.abc_classification_level_id"
    )
    def _compute_abc_classification_level_id(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.abc_classification_level_id = (
                template.product_variant_ids.abc_classification_level_id
            )
        for template in self - unique_variants:
            template.abc_classification_level_id = False

    def _inverse_abc_classification_profile_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.abc_classification_profile_id = (
                    template.abc_classification_profile_id
                )

    def _inverse_abc_classification_level_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.abc_classification_level_id = (
                    template.abc_classification_level_id
                )


class ProductProduct(models.Model):
    _inherit = "product.product"

    abc_classification_profile_id = fields.Many2one(
        "abc.classification.profile", index=True
    )
    abc_classification_level_id = fields.Many2one(
        "abc.classification.profile.level", index=True
    )
