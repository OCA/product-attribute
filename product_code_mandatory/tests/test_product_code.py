# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_model = cls.env["product.product"]
        cls.product = cls.product_model.create({"name": "Test Product Code"})

    def test_product_code(self):
        """Check Product Code"""
        self.assertTrue(self.product.default_code, "Product code is not set.")
