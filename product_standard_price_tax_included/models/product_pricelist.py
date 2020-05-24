# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.multi
    def _compute_price_rule(
            self, products_qty_partner, date=False, uom_id=False):
        ProductPricelistItem = self.env['product.pricelist.item']
        ProductProduct = self.env['product.product']
        res = super()._compute_price_rule(
            products_qty_partner, date=date, uom_id=uom_id)

        new_res = res.copy()
        for product_id, values in res.items():
            item_id = values[1]
            if item_id:
                item = ProductPricelistItem.browse(item_id)
                if item.base == 'standard_price_tax_included':
                    product = ProductProduct.browse(product_id)
                    new_res[product_id] = (
                        product.standard_price_tax_included, item_id)
        return new_res
