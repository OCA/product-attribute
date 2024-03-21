# Copyright 2017 ACSONE SA/NV
# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    tag_ids = fields.Many2many(
        comodel_name="product.template.tag",
        string="Tags",
        relation="product_product_product_tag_rel",
        column1="product_id",
        column2="tag_id",
    )
