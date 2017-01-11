# -*- coding: utf-8 -*-
# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestProductPricelistSimulation(common.SavepointCase):

    @classmethod
    def setUpClass(self):
        super(TestProductPricelistSimulation, self).setUpClass()
        self.ProductTemplate = self.env['product.template']
        self.product_template = self.ProductTemplate.create({
            'name': 'Product - template - Test',
            'type': 'consu',
            'list_price': 100.00,
        })
        ProductPriceList = self.env['product.pricelist']
        self.pricelist_1 = ProductPriceList.create({
            'name': 'test - pricelist1',
            'item_ids': [
                (0, 0, {
                    'applied_on': '3_global',
                    'fixed_price': 80.00,
                }),
            ]
        })

    def test_pricelist_simulation(self):
        html = self.product_template.pricelist_simulate
        self.assertNotEqual(html.find('100'), -1)
        self.assertNotEqual(html.find('80'), -1)
