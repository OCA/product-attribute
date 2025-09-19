# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    pricelist_item_ids = fields.One2many(
        comodel_name="product.pricelist.item",
        inverse_name="product_id",
    )
