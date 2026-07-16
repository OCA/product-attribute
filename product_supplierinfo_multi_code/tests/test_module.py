from odoo.tests.common import TransactionCase


class Test(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Supplier Test",
                "supplier_rank": 1,
            }
        )
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Customer Test",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test",
                "default_code": "INTERNAL-001",
            }
        )
        cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.supplier.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_code": "SUP-CODE-42",
            }
        )

    def test_search_by_supplier_code_without_partner_context(self):
        """Without a partner in the context, we must find the product
        via their supplier code."""
        found = self.env["product.product"].search(
            [("display_name", "ilike", "SUP-CODE-42")]
        )
        self.assertIn(self.product, found)

    def test_search_by_supplier_code_with_non_supplier_partner_context(self):
        """With a non-supplier partner in the context, the
        extended search should continue to apply."""
        found = (
            self.env["product.product"]
            .with_context(partner_id=self.customer.id)
            .search([("display_name", "ilike", "SUP-CODE-42")])
        )
        self.assertIn(self.product, found)

    def test_search_by_supplier_code_with_supplier_partner_context(self):
        """With the relevant supplier in context, the behavior
        native Odoo (already filtered on this provider) should be sufficient."""
        found = (
            self.env["product.product"]
            .with_context(partner_id=self.supplier.id)
            .search([("display_name", "ilike", "SUP-CODE-42")])
        )
        self.assertIn(self.product, found)

    def test_search_unknown_code_returns_nothing(self):
        """An unknown code should not report anything"""
        found = self.env["product.product"].search(
            [("display_name", "ilike", "NOT-EXISTING-CODE")]
        )
        self.assertNotIn(self.product, found)
