# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestProductVariantCompany(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductProduct = cls.env["product.product"]
        cls.company_1 = cls.env["res.company"].create({"name": "Company 1"})
        cls.company_2 = cls.env["res.company"].create({"name": "Company 2"})

    # Test Section
    def test_create_same_company(self):
        product_1 = self._create_product("Product 1", self.company_1)
        self.assertEqual(product_1.company_id, self.company_1)
        self.assertEqual(product_1.product_tmpl_id.company_id, self.company_1)

    def test_create_different_company(self):
        product_1 = self._create_product("Product 1", self.company_1)
        product_2 = self._create_product("Product 2", self.company_2)
        self.assertEqual(product_1.company_id, self.company_1)
        self.assertEqual(product_2.company_id, self.company_2)
        self.assertEqual(product_2.product_tmpl_id.company_id, self.company_2)

    def _create_product(self, name, company):
        vals = {
            "name": name,
            "company_id": company.id,
        }
        return self.ProductProduct.create(vals)
