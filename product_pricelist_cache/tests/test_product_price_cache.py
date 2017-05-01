# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestProductPriceCache(TransactionCase):

    def test_product_price_cache(self):
        """Check wether product price cache correctly filled and gives back
        the right values, also for non cached items.
        """
        pricelist_model = self.env['product.pricelist']
        pricelist_version_model = self.env['product.pricelist.version']
        pricelist_item_model = self.env['product.pricelist.item']
        product_model = self.env['product.product']
        cache_model = self.env['product.price.cache']
        pricelist = pricelist_model.create({
            'name': 'price cache test',
            'type': 'sale',
        })
        pricelist_version = pricelist_version_model.create({
            'pricelist_id': pricelist.id,
            'name': 'current prices',
        })
        base_sale = pricelist_item_model._get_default_base({'type': 'sale'})
        product_onsite = self.env.ref('product.product_product_1')
        product_computer = self.env.ref('product.product_product_3')
        pricelist_item_model.create({
            'price_version_id': pricelist_version.id,
            'sequence': 5,
            'base': base_sale,
            'min_quantity': 1.0,
            'price_discount': -1.0,
            'price_surcharge': 25.50,
            'product_id': product_onsite.id,
        })
        pricelist_item_model.create({
            'price_version_id': pricelist_version.id,
            'sequence': 5,
            'base': base_sale,
            'min_quantity': 1.0,
            'price_discount': -1.0,
            'price_surcharge': 35.50,
            'product_id': product_computer.id,
        })
        pricelist_item_model.create({
            'price_version_id': pricelist_version.id,
            'sequence': 5,
            'base': base_sale,
            'min_quantity': 5.0,
            'price_discount': -1.0,
            'price_surcharge': 32.25,
            'product_id': product_computer.id,
        })
        # Try to create cache
        all_products = product_onsite | product_computer
        cache_model.cache_pricelist_prices(pricelist, all_products)
        # Rebrowse first product to rebrowse
        product_one = product_model.with_context(
            pricelist=pricelist.id,
        ).browse([product_onsite.id])
        self.assertEqual(product_one.price, 25.50)
        # Rebrowse second product to rebrowse, but with quantity > 5:
        product_two = product_model.with_context(
            pricelist=pricelist.id,
            quantity=6.0,
        ).browse([product_computer.id])
        self.assertEqual(product_two.price, 32.25)
