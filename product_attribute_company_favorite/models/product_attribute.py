from odoo import models


class ProductAttribute(models.Model):
    _inherit = ["product.attribute", "product.attribute.favorite.mixin"]
    _name = "product.attribute"

    CREATION_ACROSS_COMPANY_CONFIG = (
        "product_attribute_company_favorite.new_attribute_favorite_for_all_companies"
    )
