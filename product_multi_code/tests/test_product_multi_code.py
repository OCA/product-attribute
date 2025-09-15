# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductDefaultCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.template = cls.env["product.template"].create(
            {
                "name": "Test Template",
            }
        )
        cls.product = cls.template.product_variant_id

    def test_create_basic_default_code(self):
        code = self.env["product.default_code"].create(
            {
                "name": "CODE-001",
                "product_id": self.product.id,
                "product_tmpl_id": self.template.id,
            }
        )
        self.assertEqual(code.name, "CODE-001")
        self.assertEqual(code.product_id, self.product)
        self.assertEqual(code.product_tmpl_id, self.template)

    def test_compute_product_tmpl_from_product(self):
        code = self.env["product.default_code"].create(
            {
                "name": "CODE-002",
                "product_id": self.product.id,
                "product_tmpl_id": self.template.id,
            }
        )
        self.assertEqual(code.product_tmpl_id, self.template)

    def test_compute_product_from_product_tmpl(self):
        code = self.env["product.default_code"].create(
            {
                "name": "CODE-003",
                "product_tmpl_id": self.template.id,
                "product_id": self.product.id,
            }
        )
        self.assertEqual(code.product_id, self.product)

    def test_duplicate_default_code_raises(self):
        self.env["product.default_code"].create(
            {
                "name": "DUPLICATE-CODE",
                "product_id": self.product.id,
                "product_tmpl_id": self.template.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["product.default_code"].create(
                {
                    "name": "DUPLICATE-CODE",
                    "product_id": self.product.id,
                    "product_tmpl_id": self.template.id,
                }
            )

    def test_product_or_template_required(self):
        with self.assertRaises(ValidationError) as error:
            self.env["product.default_code"].create({"name": "NO-PRODUCT"})
        self.assertIn("You must assign the internal reference", str(error.exception))
        self.assertIn("to a product or a template", str(error.exception))
