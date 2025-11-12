# Copyright 2025 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    name = fields.Char(translate=True)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        # Compute using main language defined in settings
        lang_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_category_name_translatable.complete_name_lang_id")
        )
        if lang_id:
            lang = self.env["res.lang"].browse(int(lang_id))
            if lang.exists():
                self = self.with_context(lang=lang.code)
        return super()._compute_complete_name()
