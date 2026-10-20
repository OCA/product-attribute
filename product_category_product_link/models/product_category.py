# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    product_template_ids = fields.One2many(
        "product.template", "categ_id", string="Products Templates"
    )
