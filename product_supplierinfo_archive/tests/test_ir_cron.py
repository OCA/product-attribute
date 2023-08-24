# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import fields
from odoo.tests.common import SavepointCase


class TestIrCron(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestIrCron, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.seller = cls.env.ref("product.product_supplierinfo_1")
        cls.seller.active = True
        cls.yesterday = fields.Date.subtract(fields.Date.today(), days=1)
        cls.tomorrow = fields.Date.add(fields.Date.today(), days=1)

    def test_ir_cron_date_end_tomorrow(self):
        self.assertTrue(self.seller.active)
        self.seller.date_end = self.tomorrow
        self.seller._cron_archive_product_supplierinfo()
        # Still active
        self.assertTrue(self.seller.active)

    def test_ir_cron_date_end_today(self):
        self.assertTrue(self.seller.active)
        self.seller.date_end = fields.Date.today()
        self.seller._cron_archive_product_supplierinfo()
        # Still active
        self.assertTrue(self.seller.active)

    def test_ir_cron_date_end_yesterday(self):
        self.assertTrue(self.seller.active)
        self.seller.date_end = self.yesterday
        self.seller._cron_archive_product_supplierinfo()
        # Not active anymore
        self.assertFalse(self.seller.active)
