from odoo.tests.common import TransactionCase


class TestProductCompanyDefault(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_product_company_default(self):
        product = self.env["product.product"].create({"name": "Test Product"})
        self.assertEqual(product.company_id, self.env["res.company"])
        product = (
            self.env["product.product"]
            .with_context(test_product_company_default=True)
            .create({"name": "Test Product"})
        )
        self.assertEqual(product.company_id, self.env.company)
