# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields
from odoo.tests.common import SavepointCase


class TestProductMainSupplierInfo(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductMainSupplierInfo, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_6")
        cls.seller_1 = cls.env.ref("product.product_supplierinfo_1")
        cls.seller_1.sequence = 1
        cls.seller_2 = cls.env.ref("product.product_supplierinfo_2")
        cls.seller_2.sequence = 2
        cls.seller_2bis = cls.env.ref("product.product_supplierinfo_2bis")
        cls.seller_2bis.sequence = 3
        cls.company_2 = cls.env.company.create({"name": "Company2"})

    def test_main_seller_1(self):
        """"Case 1: all the sellers share the same company."""
        self.assertEqual(self.product.main_seller_id, self.seller_1)
        self.seller_2.sequence = -1
        self.assertEqual(self.product.main_seller_id, self.seller_2)

    def test_main_seller_2(self):
        """"Case 2: the sellers do not share the same company."""
        # Assign 'seller_1' to the second company, so the main vendor computed
        # for the main company is now 'seller_2'
        self.seller_1.company_id = self.company_2
        self.assertEqual(self.product.main_seller_id, self.seller_2)
        # Check that the main vendor for the second company is 'seller_1'
        self.assertEqual(
            self.product.with_company(self.company_2).main_seller_id,
            self.seller_1,
        )

    def test_main_seller_3(self):
        """"Case 3: the sellers have different start/end dates."""
        today = fields.Date.today()
        tomorrow = fields.Date.add(today, days=1)
        yesterday = fields.Date.subtract(today, days=1)
        self.seller_1.date_start = tomorrow
        self.seller_2.date_end = yesterday
        self.assertEqual(self.product.main_seller_id, self.seller_2bis)
