# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    abc_classification_product_level_ids = fields.One2many(
        "abc.classification.product.level", index=True, inverse_name="product_id"
    )
    abc_classification_profile_ids = fields.Many2many(
        comodel_name="abc.classification.profile",
        relation="abc_classification_profile_product_rel",
        column1="product_id",
        column2="profile_id",
        index=True,
    )
    abc_classification_profile_updatable_from_category = fields.Boolean(default=True)

    def _update_abc_classification_profile_from_category(self):
        for rec in self:
            category = rec.categ_id
            if (
                not rec.abc_classification_profile_ids
                and category.abc_classification_profile_ids
            ):
                rec.abc_classification_profile_ids = (
                    category.abc_classification_profile_ids
                )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._update_abc_classification_profile_from_category()
        return res

    def write(self, vals):
        res = super().write(vals)
        if vals.get("categ_id"):
            self._update_abc_classification_profile_from_category()
        return res

    @api.onchange("categ_id")
    def _onchange_categ_id_abc_classification(self):
        self._update_abc_classification_profile_from_category()
