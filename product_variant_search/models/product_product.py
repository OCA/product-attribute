# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    variant_search_text = fields.Text(
        compute="_compute_variant_search_text",
        store=True,
        translate=True,
        index=True,
    )

    @api.depends(
        "product_tmpl_id.name",
        "default_code",
        "product_template_variant_value_ids",
    )
    def _compute_variant_search_text(self):
        for product in self:
            variant = (
                product.product_template_attribute_value_ids._get_combination_name()
            )
            base_name = product.name
            name = f"{base_name} ({variant})" if variant else base_name
            if product.default_code:
                product.variant_search_text = f"[{product.default_code}] {name}"
            else:
                product.variant_search_text = name

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = expression.AND(
            [
                args,
                [
                    "|",
                    ("variant_search_text", operator, name),
                    ("name", operator, name),
                ],
            ]
        )
        records = self.search(domain, limit=limit)
        return [(rec.id, rec.display_name or "") for rec in records]
