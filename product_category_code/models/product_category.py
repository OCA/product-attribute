# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    _rec_names_search = ["complete_name", "code"]

    code = fields.Char(
        default="/",
        index=True,
    )

    @api.depends("code")
    @api.depends_context("display_category_code", "import_compat")
    def _compute_display_name(self):
        # OVERRIDE: prefix the name with the code, like product variants.
        # Import-compatible exports keep the plain name, so they can be
        # imported back.
        super()._compute_display_name()
        if not self.env.context.get(
            "display_category_code", True
        ) or self.env.context.get("import_compat"):
            return
        for record in self:
            if record.code and record.code != "/":
                record.display_name = f"[{record.code}] {record.display_name}"

    def copy(self, default=None):
        default = default or {}
        default.setdefault("code", self.code + self.env._("-copy"))
        return super().copy(default)
