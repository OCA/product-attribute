# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_1 = cls.env.ref("product.product_product_4_product_template")
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product Code", "product_tmpl_id": cls.product_1.id}
        )

    def test_product_code(self):
        """Check Product Code"""
        self.assertTrue(self.product.default_code, "Product code is not set.")
