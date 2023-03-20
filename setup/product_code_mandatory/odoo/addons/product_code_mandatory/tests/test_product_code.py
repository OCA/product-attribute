# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    def setUp(self):
        super(TestProductCode, self).setUp()
        self.product_model = self.env["product.product"]
        self.product = self.product_model.create({"name": "Test Product Code"})

    def test_product_code(self):
        """Check Product Code"""
        self.assertTrue(self.product.default_code, "Product code is not set.")
