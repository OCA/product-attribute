# Copyright 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_optional_line_ids = fields.One2many(
        string="Optional Products Line",
        comodel_name="product.optional.line",
        inverse_name="product_tmpl_id",
    )
    optional_product_ids = fields.Many2many(
        compute="_compute_optional_product_ids",
        readonly=False,
        store=True,
    )

    @api.depends("product_optional_line_ids")
    def _compute_optional_product_ids(self):
        """
        To avoid possible issues with optional products in other modules,
        we need to compute them based on optional product lines, because
        we hide the original field.
        """
        for r in self:
            r.optional_product_ids = r.product_optional_line_ids.mapped(
                "optional_product_tmpl_id"
            )
