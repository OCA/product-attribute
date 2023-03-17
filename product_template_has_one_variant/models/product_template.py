# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    has_one_variant = fields.Boolean(
        compute="_compute_has_one_variant",
        store=True,
        index=True,
    )

    @api.depends("product_variant_ids")
    def _compute_has_one_variant(self):
        templates = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        templates.update({"has_one_variant": True})
        (self - templates).update(
            {
                "has_one_variant": False,
            }
        )
