# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    def _update_field_translations(self, field_name, translations, source_lang=None):
        res = super()._update_field_translations(
            field_name, translations, source_lang=source_lang
        )
        if field_name == "name" and translations:
            ptavs = self.env["product.template.attribute.value"].search(
                [
                    ("product_attribute_value_id", "in", self.ids),
                ]
            )
            variants = ptavs.ptav_product_variant_ids
            for lang in translations.keys():
                variants.with_context(lang=lang)._compute_variant_search_text()
        return res
