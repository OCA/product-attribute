# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import csv
import io

from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged


@tagged("-at_install", "post_install")
class TestCatalogExportController(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a user, partner, product, and pricelist for testing
        cls.user = new_test_user(cls.env, login="csv_user")
        cls.user.groups_id = [Command.link(cls.env.ref("stock.group_stock_user").id)]
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "default_code": "TP001",
                "list_price": 100.0,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Special Pricelist",
                "currency_id": cls.env.ref("base.USD").id,
            }
        )
        cls.pricelist_deafult = cls.env["product.pricelist"].create(
            {
                "name": "Deafult Pricelist",
                "currency_id": cls.env.ref("base.USD").id,
            }
        )
        cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_id": cls.product.id,
                "compute_price": "fixed",
                "fixed_price": 80.0,
            }
        )
        cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist_deafult.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_id": cls.product.id,
                "compute_price": "formula",
                "base": "list_price",
            }
        )

    def _find_product_row(self, rows, product_name):
        """Find the row in the CSV corresponding to the given product name."""
        headers = rows[0]
        name_index = headers.index("name")
        for row in rows[1:]:
            if row[name_index] == product_name:
                return row
        self.fail(f"Product {product_name} not found in CSV export")

    def _read_csv(self, content):
        """Helper to parse CSV response into rows."""
        decoded = content.decode("utf-8-sig")
        buf = io.StringIO(decoded)
        reader = csv.reader(buf)
        return list(reader)

    def test_csv_export_with_pricelist(self):
        """Export should apply pricelist and generate correct filename."""

        self.user.partner_id.property_product_pricelist = self.pricelist
        self.authenticate("csv_user", "csv_user")
        response = self.url_open("/feed/export/products.csv")
        self.assertEqual(response.status_code, 200)
        dispo = response.headers.get("Content-Disposition")
        self.assertIn("products.csv", dispo)
        self.assertTrue(dispo.endswith('.csv"'))
        rows = self._read_csv(response.content)
        headers = rows[0]
        product_row = self._find_product_row(rows, self.product.name)
        price_index = headers.index("list_price")
        price = float(product_row[price_index])
        self.assertEqual(price, 80.0)

    def test_csv_export_without_pricelist(self):
        """Export should fall back to list_price when no pricelist is assigned."""

        self.authenticate("csv_user", "csv_user")
        self.user.partner_id.property_product_pricelist = self.pricelist_deafult
        self.user.partner_id.flush_model()
        self.user.partner_id.invalidate_model()
        response = self.url_open("/feed/export/products.csv")
        self.assertEqual(response.status_code, 200)
        rows = self._read_csv(response.content)
        headers = rows[0]
        product_row = self._find_product_row(rows, self.product.name)
        price_index = headers.index("list_price")
        price = float(product_row[price_index])
        self.assertEqual(price, 100.0)
