# Copyright 2024 Akretion - David BEAL

from odoo import fields, models


class ProductCodeMixin(models.AbstractModel):
    _name = "product.code.mixin"
    _description = "Mixin to display product code in inherited models"

    product_code = fields.Char(
        related="product_id.default_code", string="Code", help="Product reference"
    )
    # The field below should already exists in your concrete model
    product_id = fields.Many2one(comodel_name="product.product")
