# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class TestSupplierinfoCode(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_6_product_template")
        cls.product_supplierinfo = cls.env.ref("product.product_supplierinfo_1")
        cls.product_supplierinfo2 = cls.env.ref("product.product_supplierinfo_2")

        # Set product code on supplierinfos
        cls.product_supplierinfo.product_code = "CODE1"
        cls.product_supplierinfo2.product_code = "CODE2"

        # Set sequence on supplierinfos
        cls.product.seller_ids.write({"sequence": 10})
        cls.product_supplierinfo.sequence = 1
        cls.product.invalidate_cache()

    def test_supplierinfo_code(self):
        """
        Check if first supplier product code is CODE1
        Search for product based on supplier_product_code
        """
        self.assertEqual(
            self.product.supplier_product_code,
            "CODE1",
        )
        product = self.product.search([("supplier_product_code", "=", "CODE1")])
        self.assertEqual(product, self.product)
        product = self.product.search([("supplier_product_code", "=", "CODE2")])
        self.assertEqual(product, self.product)
