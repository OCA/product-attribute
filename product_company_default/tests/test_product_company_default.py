from odoo.addons.base.tests.common import BaseCommon


class TestProductCompanyDefault(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Enable the configuration using ir.config_parameter
        cls.env["ir.config_parameter"].sudo().set_param(
            "product_company_default.default_company_enable", "1"
        )

    def test_product_company(self):
        # Create a sample product
        product = self.env["product.product"].create({"name": "Test Product"})
        self.assertEqual(product.company_id, self.env.company)
