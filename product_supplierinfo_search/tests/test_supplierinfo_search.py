# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSupplierinfoSearch(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Product = cls.env["product.product"]
        # Reuse any existing product when available (avoids depending on stock's
        # computed `tracking` field); create a bare one otherwise.
        cls.product = Product.search([], limit=1) or Product.create({"name": "Widget"})
        cls.vendor = cls.env["res.partner"].search([], limit=1) or cls.env[
            "res.partner"
        ].create({"name": "ACME"})
        cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.vendor.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_code": "ACME-XYZ",
                "product_name": "ACME Widget",
            }
        )

    def test_search_by_supplier_code_without_context(self):
        found = self.env["product.product"].name_search("ACME-XYZ")
        self.assertIn(self.product.id, [r[0] for r in found])

    def test_search_by_supplier_name_without_context(self):
        found = self.env["product.product"].name_search("ACME Widget")
        self.assertIn(self.product.id, [r[0] for r in found])

    def test_unrelated_search_does_not_match(self):
        found = self.env["product.product"].name_search("ZZZ-NOPE")
        self.assertNotIn(self.product.id, [r[0] for r in found])
