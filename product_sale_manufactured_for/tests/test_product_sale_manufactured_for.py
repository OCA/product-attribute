# Copyright 2023 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductSaleManufacturedFor(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.customer1 = cls.env.ref("base.res_partner_4")
        cls.customer2 = cls.env.ref("base.res_partner_3")
        cls.product = cls.env.ref("product.product_product_4")
        cls.product2 = cls.env.ref("product.product_product_5")

    def test_archiving_customer(self):
        """Check archiving a customer cleans the product manufactured for field."""
        self.product.manufactured_for_partner_ids = [(4, self.customer1.id, 0)]
        self.product2.manufactured_for_partner_ids = [
            (4, self.customer1.id, 0),
            (4, self.customer2.id, 0),
        ]
        self.assertTrue(self.customer1 in self.product.manufactured_for_partner_ids)
        self.customer1.active = False
        self.assertFalse(self.customer1 in self.product.manufactured_for_partner_ids)
        self.assertFalse(self.customer1 in self.product2.manufactured_for_partner_ids)
        self.assertTrue(self.customer2 in self.product2.manufactured_for_partner_ids)
