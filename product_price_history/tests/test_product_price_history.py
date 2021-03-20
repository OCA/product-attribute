# coding: utf-8
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp.tests.common import SavepointCase


class TestProductPriceHistory(SavepointCase):

    def test_01_price_history_count(self):
        """ Price history count is updated correctly """
        product = self.env.ref('product.product_product_17')
        template = product.product_tmpl_id
        self.assertEqual(template.product_variant_count, 1)

        product_count = product.price_history_count
        template_count = template.price_history_count

        template.standard_price = 100.0
        template._compute_price_history_count()
        product._compute_price_history_count()
        self.assertEqual(template.price_history_count, template_count + 1)
        self.assertEqual(product.price_history_count, product_count + 1)

        product.standard_price = 200.0
        product._compute_price_history_count()
        template._compute_price_history_count()
        self.assertEqual(product.price_history_count, product_count + 2)
        self.assertEqual(template.price_history_count, template_count + 2)

        new_product = self.env["product.product"]\
            .with_context(recompute=False)\
            .create({'product_tmpl_id': template.id, 'standard_price': 123.0})
        new_product._compute_price_history_count()
        product._compute_price_history_count()
        template._compute_price_history_count()
        self.assertEqual(new_product.price_history_count, product_count + 3)
        self.assertEqual(product.price_history_count, product_count + 3)
        self.assertEqual(template.price_history_count, template_count + 3)
