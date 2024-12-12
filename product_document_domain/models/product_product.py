# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_product_document_count(self):
        res = super()._compute_product_document_count()
        for product in self:
            template = product.product_tmpl_id
            product.product_document_count += product.env[
                "product.document"
            ].search_count(
                [
                    ("res_model", "=", "product.template"),
                    ("res_id", "=", template.id),
                ]
            )
        return res

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
