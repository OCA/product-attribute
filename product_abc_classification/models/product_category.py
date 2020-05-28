# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    abc_classification_profile_id = fields.Many2one("abc.classification.profile")
    product_variant_ids = fields.One2many("product.product", inverse_name="categ_id")

    @api.onchange("abc_classification_profile_id")
    def _onchange_abc_classification_profile_id(self):
        for categ in self:
            for child in categ._origin.child_id:
                child.abc_classification_profile_id = (
                    categ.abc_classification_profile_id
                )
                child._onchange_abc_classification_profile_id()
            for variant in categ._origin.product_variant_ids.filtered(
                lambda p: p.type == "product"
            ):
                variant.abc_classification_profile_id = (
                    categ.abc_classification_profile_id
                )
