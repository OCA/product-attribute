from odoo.addons.base.tests.common import BaseCommon


class TestProductSupplierinfoIndirectCost(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Vendor",
            }
        )

    def test_indirect_cost_amount_computation(self):
        supplierinfo = self.env["product.supplierinfo"].create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "partner_id": self.partner.id,
                "price": 100.0,
                "indirect_cost_percent": 10.0,
            }
        )
        self.assertEqual(supplierinfo.indirect_cost_amount, 10.0)
