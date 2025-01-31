# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_product_document_count(self):
        for template in self:
            res = super()._compute_product_document_count()
            template.product_document_count -= template.env[
                "product.document"
            ].search_count(
                [
                    ("res_model", "=", "product.product"),
                    ("res_id", "in", template.product_variant_ids.ids),
                ]
            )
            return res

    def action_open_documents(self):
        res = super().action_open_documents()
        res["context"].update(
            {
                "search_default_context_template": True,
            }
        )
        return res
