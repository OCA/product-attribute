# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_product_document_count(self):
        super()._compute_product_document_count()
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            return
        variant_doc_groups = self.env["product.document"].read_group(
            domain=[
                ("res_model", "=", "product.product"),
                ("res_id", "in", all_variant_ids),
            ],
            fields=["res_id"],
            groupby=["res_id"],
        )
        count_by_variant = {g["res_id"]: g["res_id_count"] for g in variant_doc_groups}
        for template in self:
            variant_doc_count = sum(
                count_by_variant.get(vid, 0) for vid in template.product_variant_ids.ids
            )
            template.product_document_count -= variant_doc_count

    def action_open_documents(self):
        res = super().action_open_documents()
        res["context"].update(
            {
                "search_default_context_template": True,
            }
        )
        return res
