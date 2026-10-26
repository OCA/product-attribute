from odoo import fields, models


class ProductAttribute(models.Model):
    _name = "product.attribute"
    _inherit = ["product.attribute", "product.sticker.mixin"]

    sticker_ids = fields.One2many(
        inverse_name="product_attribute_id",
    )
