from odoo import models


class ProductAttributeValue(models.Model):
    _inherit = ["product.attribute.value", "product.attribute.favorite.mixin"]
    _name = "product.attribute.value"

    CREATION_ACROSS_COMPANY_CONFIG = (
        "product_attribute_company_favorite."
        "new_attribute_value_favorite_for_all_companies"
    )
