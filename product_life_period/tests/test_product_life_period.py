# -*- coding: utf-8 -*-
# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

import openerp.tests.common as common
from openerp import fields


class TestProductLifePeriod(common.TransactionCase):

    def test_end_period(self):
        """ Check at the end of period product are set in state end and
            period is set inactive
        """
        date_today = fields.Date.from_string(fields.Date.today())
        product_life_period_obj = self.env['product.life.period']
        # create a passed life period
        passed_date = date_today + timedelta(days=-5)
        product_life_passed = product_life_period_obj.create(
            {'name': 'Passed period',
             'end_date': passed_date})
        # create a future life period
        future_date = date_today + timedelta(days=5)
        product_life_future = product_life_period_obj.create(
            {'name': 'Future period',
             'end_date': future_date})
        # set product in each period
        product1 = self.env.ref('product.product_product_36')
        product2 = self.env.ref('product.product_product_37')
        product3 = self.env.ref('product.product_product_38')
        product1.product_life_period_id = product_life_passed.id
        product2.product_life_period_id = product_life_future.id

        # run scheduler
        product_life_period_obj._run_life_period_update()

        self.assertEqual(product1.state, 'end')
        self.assertFalse(product2.state)
        self.assertFalse(product3.state)
        self.assertFalse(product_life_passed.active)
        self.assertTrue(product_life_future.active)
