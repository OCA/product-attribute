# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_price_uom_reference(self, product, pricelist):
        product_price = pricelist._get_product_price(
            product, 1, currency=pricelist.currency_id or product.currency_id
        )
        if product.uom_reference_id:
            return product_price / product.uom_reference_id.ratio
        return False
