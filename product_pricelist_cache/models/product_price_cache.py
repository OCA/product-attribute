# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class ProductPriceCache(models.Model):
    _name = 'product.price.cache'
    _order = 'pricelist_id, product_id'

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        ondelete='cascade',
        readonly=True,
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        ondelete='cascade',
        readonly=True,
        index=True,
    )
    price = fields.Float(
        digits=dp.get_precision('Product Price'),
        readonly=True,
    )

    @api.model
    def cache_pricelist_prices(self, pricelist, all_products):
        """Cache all simple product prices for a single pricelist."""
        pricelist_model = self.env['product.pricelist']
        for product in all_products:
            product_prices = pricelist_model.with_context(
                no_cache=True
            )._price_get_multi(pricelist, [(product, 1.0, False)])
            product_price = \
                product_prices and product_prices.get(product.id, 0.0) or \
                0.0
            product_cache = self.search([
                ('pricelist_id', '=', pricelist.id),
                ('product_id', '=', product.id),
            ])
            if product_cache:
                product_cache.write({'price': product_price})
            else:
                product_cache.create({
                    'pricelist_id': pricelist.id,
                    'product_id': product.id,
                    'price': product_price,
                })

    @api.model
    def cache_pricelist_prices_all(self):
        """Cache prices for all pricelists, for all products."""
        product_model = self.env['product.product']
        pricelist_model = self.env['product.pricelist']
        all_products = product_model.search([('sale_ok', '=', True)])
        all_pricelists = pricelist_model.search([('type', '=', 'sale')])
        for pricelist in all_pricelists:
            self.cache_pricelist_prices(pricelist, all_products)
