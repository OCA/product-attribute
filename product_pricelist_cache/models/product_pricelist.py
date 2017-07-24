# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.model
    def _price_get_multi(self, pricelist, products_by_qty_by_partner):
        if self.env.context.get('no_cache', False):
            return super(ProductPricelist, self)._price_get_multi(
                pricelist, products_by_qty_by_partner
            )
        cache_model = self.env['product.price.cache']
        results = {}
        non_cached_pqp = []
        for product, qty, partner in products_by_qty_by_partner:
            price_found = False
            qty = qty == 0.0 and 1.0 or qty
            if qty == 1.0 and not partner:
                # Can use default price for list
                cached_price = cache_model.search([
                    ('product_id', '=', product.id),
                    ('pricelist_id', '=', pricelist.id),
                ])
                if cached_price:
                    price_found = True
                    results[product.id] = cached_price[0].price
            if not price_found:
                non_cached_pqp.append((product, qty, partner))
        if non_cached_pqp:
            non_cached_results = super(
                ProductPricelist, self
            )._price_get_multi(pricelist, non_cached_pqp)
            results.update(non_cached_results)
        return results
