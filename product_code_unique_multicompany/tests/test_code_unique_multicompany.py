# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestCodeUniqueMulticompany(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company_1 = self.env.ref("base.main_company")
        self.company_2 = self.env["res.company"].create({"name": "Company 2"})
        self.product_1 = self.env["product.product"].search([], limit=1)
        self.product_1.default_code = "TESTCODE1"
        self.product_1.company_id = self.company_1

    def test_different_code_same_company(self):
        self.product_2 = self.env["product.product"].create(
            {
                "name": "Test Product 2",
                "default_code": "TESTCODE2",
                "company_id": self.company_1.id,
            }
        )

    def test_same_code_different_company(self):
        self.product_2 = self.env["product.product"].create(
            {
                "name": "Test Product 2",
                "default_code": "TESTCODE1",
                "company_id": self.company_2.id,
            }
        )

    def test_same_code_same_company(self):
        with self.assertRaises(UniqueViolation), mute_logger("odoo.sql_db"):
            self.product_2 = self.env["product.product"].create(
                {
                    "name": "Test Product 2",
                    "default_code": "TESTCODE1",
                    "company_id": self.company_1.id,
                }
            )
