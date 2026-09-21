# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    tag_ids = fields.Many2many(
        comodel_name="product.category.tag",
        relation="product_category_tag_rel",
        column1="category_id",
        column2="tag_id",
        string="Tags",
    )
