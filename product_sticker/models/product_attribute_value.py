from odoo import fields, models


class ProductAttributeValue(models.Model):
    _name = "product.attribute.value"
    _inherit = ["product.attribute.value", "product.sticker.mixin"]

    sticker_ids = fields.One2many(
        inverse_name="product_attribute_value_id",
    )
