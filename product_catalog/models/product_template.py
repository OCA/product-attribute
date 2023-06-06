# Copyright 2023 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy<raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_catalog_ids = fields.Many2many(
        "product.catalog", compute="_compute_product_catalog_ids", readonly=True
    )

    def _compute_product_catalog_ids(self):
        for rec in self:
            rec.product_catalog_ids = rec.product_variant_ids.mapped(
                "product_catalog_ids"
            )
