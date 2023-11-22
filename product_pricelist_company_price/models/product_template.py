#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_in_products_pricelist = fields.Boolean(
        compute="_compute_is_in_products_pricelist",
    )

    def _compute_is_in_products_pricelist(self):
        product_model = self.env["product.product"]
        for product in self:
            is_in_products_pricelist = product_model._is_in_products_pricelist(product)
            product.is_in_products_pricelist = is_in_products_pricelist
