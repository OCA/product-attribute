# Copyright 2025 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _active_languages(self):
        return self.env["res.lang"].search([]).ids

    def _default_language(self):
        lang_code = self.env["ir.default"]._get("res.partner", "lang")
        def_lang_id = self.env["res.lang"]._get_data(code=lang_code).id
        return def_lang_id or self._active_languages()[0]

    product_category_complete_name_lang_id = fields.Many2one(
        "res.lang",
        string="Product Category Complete Name Language",
        default=lambda self: self._default_language(),
        required=True,
        config_parameter="product_category_name_translatable.complete_name_lang_id",
    )

    def set_values(self):
        old_lang = self.default_get(["product_category_complete_name_lang_id"])[
            "product_category_complete_name_lang_id"
        ]
        res = super().set_values()
        if (
            self.product_category_complete_name_lang_id
            and self.product_category_complete_name_lang_id.id != old_lang
        ):
            # Recompute complete names
            self.env["product.category"].sudo().search([])._compute_complete_name()
        return res
