# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = "product.template"

    medical_usage = fields.Html(
        compute="_compute_medical_usage",
        inverse="_inverse_medical_usage",
        store=True,
        translate=html_translate,
    )
    medical_contra_indication = fields.Html(
        compute="_compute_medical_contra_indication",
        inverse="_inverse_medical_contra_indication",
        store=True,
        translate=html_translate,
    )
    medical_properties = fields.Html(
        compute="_compute_medical_properties",
        inverse="_inverse_medical_properties",
        store=True,
        translate=html_translate,
    )
    medical_composition = fields.Html(
        compute="_compute_medical_composition",
        inverse="_inverse_medical_composition",
        store=True,
        translate=html_translate,
    )
    medical_full_description = fields.Html(
        compute="_compute_medical_full_description",
        inverse="_inverse_medical_full_description",
        store=True,
        translate=html_translate,
    )
    medical_indication = fields.Html(
        compute="_compute_medical_indication",
        inverse="_inverse_medical_indication",
        store=True,
        translate=html_translate,
    )
    medical_nutritional_value = fields.Html(
        compute="_compute_medical_nutritional_value",
        inverse="_inverse_medical_nutritional_value",
        store=True,
        translate=html_translate,
    )
    medical_legal_text = fields.Html(
        compute="_compute_medical_legal_text",
        inverse="_inverse_medical_legal_text",
        store=True,
        translate=html_translate,
    )

    @api.depends("product_variant_ids.medical_usage")
    def _compute_medical_usage(self):
        self._compute_template_field_from_variant_field("medical_usage")

    def _inverse_medical_usage(self):
        self._set_product_variant_field("medical_usage")

    @api.depends("product_variant_ids.medical_contra_indication")
    def _compute_medical_contra_indication(self):
        self._compute_template_field_from_variant_field("medical_contra_indication")

    def _inverse_medical_contra_indication(self):
        self._set_product_variant_field("medical_contra_indication")

    @api.depends("product_variant_ids.medical_properties")
    def _compute_medical_properties(self):
        self._compute_template_field_from_variant_field("medical_properties")

    def _inverse_medical_properties(self):
        self._set_product_variant_field("medical_properties")

    @api.depends("product_variant_ids.medical_composition")
    def _compute_medical_composition(self):
        self._compute_template_field_from_variant_field("medical_composition")

    def _inverse_medical_composition(self):
        self._set_product_variant_field("medical_composition")

    @api.depends("product_variant_ids.medical_full_description")
    def _compute_medical_full_description(self):
        self._compute_template_field_from_variant_field("medical_full_description")

    def _inverse_medical_full_description(self):
        self._set_product_variant_field("medical_full_description")

    @api.depends("product_variant_ids.medical_nutritional_value")
    def _compute_medical_nutritional_value(self):
        self._compute_template_field_from_variant_field("medical_nutritional_value")

    def _inverse_medical_nutritional_value(self):
        self._set_product_variant_field("medical_nutritional_value")

    @api.depends("product_variant_ids.medical_indication")
    def _compute_medical_indication(self):
        self._compute_template_field_from_variant_field("medical_indication")

    def _inverse_medical_indication(self):
        self._set_product_variant_field("medical_indication")

    @api.depends("product_variant_ids.medical_legal_text")
    def _compute_medical_legal_text(self):
        self._compute_template_field_from_variant_field("medical_legal_text")

    def _inverse_medical_legal_text(self):
        self._set_product_variant_field("medical_legal_text")
