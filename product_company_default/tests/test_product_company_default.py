from odoo.tests.common import TransactionCase


class TestProductCompanyDefault(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductCompanyDefault, cls).setUpClass()
        # Enable the configuration using ir.config_parameter
        cls.env["ir.config_parameter"].sudo().set_param(
            "product_company_default.default_company_enable", "1"
        )

    def test_product_company(self):
        # Create a sample product
        product = self.env["product.product"].create({"name": "Test Product"})
        self.assertEqual(product.company_id, self.env.company)
