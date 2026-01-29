# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        # New variants can be created/updated when changing attribute lines.
        # Existing translations won't trigger `_update_field_translations()`,
        # so we recompute per language to store translated `variant_search_text`.
        templates._recompute_variant_search_text_all_langs()
        return templates

    def write(self, vals):
        res = super().write(vals)
        if "attribute_line_ids" in vals:
            self._recompute_variant_search_text_all_langs()
        return res

    def _recompute_variant_search_text_all_langs(self):
        langs = self.env["res.lang"].search([("active", "=", True)]).mapped("code")
        variants = self.product_variant_ids
        for lang in langs:
            variants.with_context(lang=lang)._compute_variant_search_text()

    def _update_field_translations(self, field_name, translations, source_lang=None):
        res = super()._update_field_translations(
            field_name, translations, source_lang=source_lang
        )
        if field_name == "name" and translations:
            variants = self.product_variant_ids
            for lang in translations.keys():
                variants.with_context(lang=lang)._compute_variant_search_text()
        return res
