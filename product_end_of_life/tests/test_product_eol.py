# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from odoo.addons.product.tests.common import TestProductCommon


class TestProductEol(TestProductCommon):

    @classmethod
    def setUpClass(cls):
        super(TestProductEol, cls).setUpClass()

        today = date.today()
        cls.Product = cls.env['product.product']

        cls.product_2.write(
            {'eol_date': today + relativedelta(months=1),
             'type': 'product'})
        cls.product_3.write(
            {'eol_date': today + relativedelta(months=1, days=1),
             'type': 'product'})
        cls.product_4.write(
            {'eol_date': today + relativedelta(months=1, days=-1),
             'type': 'product'})
        cls.product_5.write(
            {'eol_date': today - relativedelta(weeks=1),
             'type': 'product'})

    def test_name_search(self):
        res_without_ctx = self.Product.name_search(self.product_5.name)
        self.assertEqual(len(res_without_ctx), 1)

        res_with_ctx = self.Product.with_context(
            {'source_from': 'purchase_order'}
        ).name_search(self.product_5.name)
        self.assertEqual(len(res_with_ctx), 0)

    def test_search_read(self):
        domain_subset = [
            self.product_2.id,
            self.product_3.id,
            self.product_4.id,
            self.product_5.id
        ]

        res_without_ctx = self.Product.search_read(
            domain=[('id', 'in', domain_subset)])
        self.assertEqual(len(res_without_ctx), 4)

        res_with_ctx = self.Product.with_context(
            {'source_from': 'purchase_order'}
        ).search_read(domain=[('id', 'in', domain_subset)])
        self.assertEqual(len(res_with_ctx), 3)

    def test_notify_products(self):
        self.Product.send_notify_product_eol()
        cron = self.env.ref('product_end_of_life.ir_cron_notify_product_eol')
        self.assertEqual(cron.interval_number, 1)
        self.assertEqual(cron.interval_type, 'months')
        self.assertEqual(
            cron.nextcall,
            datetime.combine(date.today() + relativedelta(months=1),
                             datetime.min.time())
        )
