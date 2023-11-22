#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_in_products_pricelist = fields.Boolean(
        compute="_compute_is_in_products_pricelist",
    )

    @api.model
    def _is_in_products_pricelist(self, product):
        """Determine if `product` (template or variant) is in the Company pricelist."""
        now = fields.Datetime.now()
        company = product.company_id or product.env.company
        products_pricelist = company.products_price_pricelist_id
        if products_pricelist:
            products_pricelist_items = products_pricelist._get_applicable_rules(
                product, now
            )
            products_pricelist_items = products_pricelist_items.filtered(
                lambda rule: rule._is_products_pricelist_item()
            )
            is_in_products_pricelist = bool(products_pricelist_items)
        else:
            is_in_products_pricelist = False
        return is_in_products_pricelist

    def _compute_is_in_products_pricelist(self):
        for product in self:
            is_in_products_pricelist = self._is_in_products_pricelist(product)
            product.is_in_products_pricelist = is_in_products_pricelist
