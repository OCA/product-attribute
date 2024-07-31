# Copyright 2024 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    abc_classification_profile_ids = fields.Many2many(
        comodel_name="abc.classification.profile",
        relation="abc_classification_profile_product_categ_rel",
        column1="categ_id",
        column2="profile_id",
        index=True,
    )

    def update_product_abc_classification_profile(self):
        for categ in self:
            products = self.env["product.product"].search(
                [
                    ("categ_id", "=", categ.id),
                    ("abc_classification_profile_updatable_from_category", "=", True),
                ]
            )
            if products:
                products.write(
                    {
                        "abc_classification_profile_ids": [
                            (6, 0, categ.abc_classification_profile_ids.ids)
                        ]
                    }
                )
