# -*- coding: utf-8 -*-
# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    abc_classification_profile_ids = fields.Many2many(
        "abc.classification.profile",
        compute="_compute_abc_classification_profile_ids",
        inverse="_inverse_abc_classification_profile_ids",
        store=True,
    )
    abc_classification_product_level_ids = fields.One2many(
        "abc.classification.product.level",
        compute="_compute_abc_classification_product_level_ids",
        inverse="_inverse_abc_classification_product_level_ids",
        inverse_name="product_tmpl_id",
        store=True,
    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.abc_classification_profile_ids",
    )
    def _compute_abc_classification_profile_ids(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.abc_classification_profile_ids = (
                template.product_variant_ids.abc_classification_profile_ids
            )
        for template in self - unique_variants:
            template.abc_classification_profile_ids = False

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.abc_classification_product_level_ids",
    )
    def _compute_abc_classification_product_level_ids(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            variants = template.product_variant_ids
            template.abc_classification_product_level_ids = \
                variants.abc_classification_product_level_ids
        for template in self - unique_variants:
            template.abc_classification_product_level_ids = False

    def _inverse_abc_classification_profile_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                variants = template.product_variant_ids
                variants.abc_classification_profile_ids = \
                    template.abc_classification_profile_ids

    def _inverse_abc_classification_product_level_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                variants = template.product_variant_ids
                variants.abc_classification_product_level_ids = \
                    template.abc_classification_product_level_ids
