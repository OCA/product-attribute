# Copyright 2020 Versada UAB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    attribute_line_ids = fields.One2many(
        comodel_name="product.category.attribute.line",
        inverse_name="category_id",
        string="Allowed Attributes",
    )
