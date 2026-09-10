# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_product_document_count(self):
        super()._compute_product_document_count()
        all_template_ids = self.mapped("product_tmpl_id").ids
        if not all_template_ids:
            return
        tmpl_doc_groups = self.env["product.document"].read_group(
            domain=[
                ("res_model", "=", "product.template"),
                ("res_id", "in", all_template_ids),
            ],
            fields=["res_id"],
            groupby=["res_id"],
        )
        count_by_template = {g["res_id"]: g["res_id_count"] for g in tmpl_doc_groups}
        for product in self:
            tmpl_count = count_by_template.get(product.product_tmpl_id.id, 0)
            product.product_document_count += tmpl_count

    def action_open_documents(self):
        res = super().action_open_documents()
        res["context"].update(
            {
                "default_parent_res_id": self.product_tmpl_id.id,
                "search_default_context_variant": False,
                "search_default_context_template": False,
                "search_default_context_variant_template": True,
            }
        )
        return res
